from __future__ import annotations

import sys
import json
import re
import subprocess
import unittest
from pathlib import Path

import chess
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT.parent
sys.path.insert(0, str(ROOT / "scripts"))

from common import elo_band, fen4, load_manifest, parse_pgn_games  # noqa: E402
from maia3_profile import fen6, normalized_entropy, position_from_fixed_prefix, set_position_from_record  # noqa: E402
from score_candidates import build_scorecards  # noqa: E402
from validate_course import validate  # noqa: E402


class CommonTests(unittest.TestCase):
    def test_fen4(self):
        self.assertEqual(fen4(chess.Board()), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")

    def test_elo_band(self):
        bands=[(1100,1299),(1300,1499)]
        self.assertEqual(elo_band(1300,bands),(1300,1499))
        self.assertIsNone(elo_band(900,bands))

    def test_entropy(self):
        self.assertAlmostEqual(normalized_entropy([0.5,0.5]),1.0)
        self.assertAlmostEqual(normalized_entropy([1.0]),0.0)


class FakeMaiaEngine:
    def __init__(self):
        self.board = chess.Board()
        self.commands = []

    def cmd_position(self, command: str) -> None:
        self.commands.append(command)
        parts = command.split()
        if command.startswith("position startpos"):
            self.board = chess.Board()
            if "moves" in parts:
                for uci in parts[parts.index("moves") + 1:]:
                    self.board.push(chess.Move.from_uci(uci))
            return
        if command.startswith("position fen"):
            fen = " ".join(parts[2:8])
            self.board = chess.Board(fen)
            if "moves" in parts[8:]:
                for uci in parts[parts.index("moves") + 1:]:
                    self.board.push(chess.Move.from_uci(uci))
            return
        raise ValueError(command)


class MaiaPositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest(COURSE/"DATA/core_40_index.csv")

    def test_fen6_normalizes_four_fields_and_rejects_bad_fen(self):
        self.assertEqual(fen6("8/8/8/8/8/8/8/8 w - -"), "8/8/8/8/8/8/8/8 w - - 0 1")
        self.assertEqual(fen6("8/8/8/8/8/8/8/8 w - - 7 42"), "8/8/8/8/8/8/8/8 w - - 7 42")
        with self.assertRaises(ValueError):
            fen6("8/8/8/8/8/8/8/8 w -")

    def test_all_fixed_prefixes_reconstruct_manifest_target_positions(self):
        self.assertEqual(len(self.manifest), 40)
        for rec in self.manifest.to_dict("records"):
            board, history = position_from_fixed_prefix(rec)
            self.assertEqual(fen4(board), fen4(rec["fen_after_key_move"]), rec["line_id"])
            self.assertEqual(board.turn, chess.Board(fen6(rec["fen_after_key_move"])).turn, rec["line_id"])
            self.assertTrue(history, rec["line_id"])
            self.assertNotEqual(fen4(board), fen4(chess.Board()), rec["line_id"])

    def test_set_position_from_record_uses_startpos_moves_and_legal_target_moves(self):
        for rec in self.manifest.to_dict("records"):
            engine = FakeMaiaEngine()
            set_position_from_record(engine, rec)
            self.assertTrue(engine.commands[-1].startswith("position startpos moves "), rec["line_id"])
            self.assertEqual(fen4(engine.board), fen4(rec["fen_after_key_move"]), rec["line_id"])
            legal = {move.uci() for move in engine.board.legal_moves}
            self.assertTrue(legal, rec["line_id"])
            self.assertNotIn(rec["key_move_uci"], legal, rec["line_id"])

    def test_bdg_01_not_left_on_initial_position(self):
        rec = self.manifest[self.manifest["line_id"] == "BDG-01"].iloc[0].to_dict()
        engine = FakeMaiaEngine()
        set_position_from_record(engine, rec)
        legal = {move.uci() for move in engine.board.legal_moves}
        self.assertEqual(fen4(engine.board), fen4(rec["fen_after_key_move"]))
        self.assertTrue({"e2e4", "d2d4", "c2c4"}.isdisjoint(legal))


class ScorecardGateTests(unittest.TestCase):
    def test_scorecards_expose_separate_gates_and_do_not_sum_duplicate_response_totals(self):
        df = build_scorecards(
            COURSE/"DATA/core_40_index.csv",
            COURSE/"DATA/stockfish_v1_500k.csv",
            COURSE/"DATA/maia3_79m_evaluated_corrected.csv",
            COURSE/"DATA/lichess_test_expanded.csv",
            COURSE/"DATA/lichess_test_expanded_evaluated.csv",
        )
        required = {
            "evidence_status",
            "engine_gate",
            "empirical_sample_gate",
            "maia_status",
            "editorial_recommendation",
            "empirical_total_after_key",
            "empirical_groups_observed",
            "empirical_elo_bands_observed",
            "empirical_speeds_observed",
        }
        self.assertTrue(required <= set(df.columns))
        ld = pd.read_csv(COURSE/"DATA/lichess_test_expanded.csv")
        expected = (
            ld[ld["position_role"] == "after_key"]
            .drop_duplicates(["line_id", "elo_min", "elo_max", "speed", "split"])
            .groupby("line_id")["total_positions"]
            .sum()
        )
        for line_id, total in expected.items():
            got = int(df.loc[df["line_id"] == line_id, "empirical_total_after_key"].iloc[0])
            self.assertEqual(got, int(total), line_id)

    def test_engine_reject_is_never_editorial_review_ready(self):
        df = build_scorecards(
            COURSE/"DATA/core_40_index.csv",
            COURSE/"DATA/stockfish_v1_500k.csv",
            COURSE/"DATA/maia3_79m_evaluated_corrected.csv",
            COURSE/"DATA/lichess_test_expanded.csv",
            COURSE/"DATA/lichess_test_expanded_evaluated.csv",
        )
        rejected = df[df["engine_gate"] == "REJECT"]
        self.assertTrue(len(rejected) > 0)
        self.assertFalse((rejected["editorial_recommendation"] == "EDITORIAL_REVIEW_READY").any())


class EditorialV11Tests(unittest.TestCase):
    def test_editorial_v11_artifacts_are_consistent(self):
        key_path = COURSE / "DATA/key_move_audit_v1_1.csv"
        failure_path = COURSE / "DATA/continuation_failure_audit_v1_1.csv"
        repairs_path = COURSE / "DATA/continuation_repair_candidates_v1_1.csv"
        decisions_path = COURSE / "DATA/editorial_line_decisions_v1_1.csv"
        candidate_manifest_path = COURSE / "DATA/core_v1_1_candidate_manifest.csv"
        candidate_pgn_path = COURSE / "PGN/99_cours_v1_1_candidate.pgn"
        for path in [key_path, failure_path, repairs_path, decisions_path, candidate_manifest_path, candidate_pgn_path, COURSE / "PRODUCTION/RAPPORT_REFONTE_EDITORIALE_V1_1.md"]:
            self.assertTrue(path.exists(), path)

        key = pd.read_csv(key_path)
        self.assertEqual(len(key), 40)
        self.assertFalse(key["key_move_san"].isna().any())
        self.assertTrue(set(key["key_move_gate"]) <= {"PASS", "REVIEW", "REJECT"})
        for row in key.to_dict("records"):
            loss = int(row["key_move_loss_cp"])
            expected = "PASS" if loss <= 25 else "REVIEW" if loss <= 50 else "REJECT"
            self.assertEqual(row["key_move_gate"], expected, row["line_id"])

        failures = pd.read_csv(failure_path)
        self.assertEqual(len(failures), 40)
        self.assertTrue(set(failures["failure_type"]) <= {"NO_ENGINE_FAILURE", "KEY_MOVE_FAILURE", "LATER_CONTINUATION_REVIEW", "LATER_CONTINUATION_REJECT"})
        for row in failures.to_dict("records"):
            if row["failure_type"] == "KEY_MOVE_FAILURE":
                self.assertIn(row["key_move_gate"], {"REVIEW", "REJECT"})
            if row["failure_type"] == "LATER_CONTINUATION_REJECT":
                self.assertGreater(int(row["first_black_loss_over_50"]), 50)

        repairs = pd.read_csv(repairs_path)
        self.assertTrue(set(repairs.get("concept_preserved", pd.Series(dtype=str)).dropna()) <= {"YES", "PARTIAL", "NO"})
        self.assertTrue(set(repairs.get("repair_complexity", pd.Series(dtype=str)).dropna()) <= {"SIMPLE", "MODERATE", "COMPLEX"})

        decisions = pd.read_csv(decisions_path)
        self.assertEqual(len(decisions), 40)
        self.assertFalse(((decisions["decision"] == "KEEP_CORE") & (decisions["key_move_gate"] == "REJECT")).any())

        cand = pd.read_csv(candidate_manifest_path)
        self.assertGreaterEqual(len(cand), 20)
        self.assertLessEqual(len(cand), 24)
        self.assertEqual(len(cand["line_id_v1_1"]), len(set(cand["line_id_v1_1"])))
        games = list(parse_pgn_games(candidate_pgn_path))
        self.assertEqual(len(games), len(cand))
        manifest_ids = set(cand["line_id_v1_1"])
        pgn_ids = {game.headers.get("Round") for game in games}
        self.assertEqual(pgn_ids, manifest_ids)
        candidate_sf = pd.read_csv(COURSE / "DATA/stockfish_v1_1_candidate_500k.csv")
        self.assertFalse((candidate_sf["loss_for_black_cp"].astype(int) > 25).any())
        self.assertEqual(set(candidate_sf["line_id"]), manifest_ids)
        for game in games:
            self.assertFalse(game.errors, game.headers.get("Round"))
            board = game.board()
            line_id = game.headers.get("Round")
            sf_line = candidate_sf[candidate_sf["line_id"] == line_id]
            for node in game.mainline():
                self.assertIn(node.move, board.legal_moves, game.headers.get("Round"))
                if board.turn == chess.BLACK:
                    match = sf_line[(sf_line["fen_before"].map(fen4) == fen4(board)) & (sf_line["move_uci"] == node.move.uci())]
                    if not match.empty:
                        self.assertLessEqual(int(match.iloc[0]["loss_for_black_cp"]), 25, (line_id, node.ply(), node.move.uci()))
                board.push(node.move)
    def test_v11_strict_editorial_rules_and_evidence(self):
        decisions = pd.read_csv(COURSE / "DATA/editorial_line_decisions_v1_1.csv")
        cand = pd.read_csv(COURSE / "DATA/core_v1_1_candidate_manifest.csv")
        repairs = pd.read_csv(COURSE / "DATA/continuation_repair_candidates_v1_1.csv")
        self.assertFalse(((decisions["decision"] == "KEEP_CORE") & (decisions["failure_type"] != "NO_ENGINE_FAILURE")).any())
        self.assertFalse(cand["continuation_gate"].isin(["LATER_CONTINUATION_REVIEW", "LATER_CONTINUATION_REJECT"]).any())
        for col in ["maia_status", "lichess_exact_position_status", "empirical_total_after_key", "empirical_sample_gate", "maia_human_error_proxy", "practical_edge_score"]:
            self.assertIn(col, decisions.columns)
            self.assertFalse((decisions[col].astype(str) == "NON_EXECUTE").any(), col)
        expected = {"ORD-01": "f7f6", "COL-10": "d8c7", "LON-04": "a8c8", "LON-03": "c8f5", "LON-07": "c8f5", "TOR-05": "d8b6"}
        for line_id, move in expected.items():
            match = repairs[(repairs["line_id"] == line_id) & (repairs["replacement_move_uci"] == move)]
            self.assertFalse(match.empty, (line_id, move))
            self.assertLessEqual(int(match.iloc[0]["replacement_loss_cp"]), 25)
            self.assertEqual(match.iloc[0]["concept_preserved"], "YES")

    def test_v11_repair_fens_bilans_selection_and_composition(self):
        expected_source_ids = [
            "ORD-01", "ORD-02", "COL-01", "COL-10", "VER-01", "LON-02", "LON-04", "LON-09", "LON-01", "LON-03",
            "LON-05", "JOB-09", "PST-04", "LON-12", "TOR-02", "PST-01", "LON-07", "TOR-06", "TOR-05", "JOB-04",
        ]
        cand = pd.read_csv(COURSE / "DATA/core_v1_1_candidate_manifest.csv")
        repairs = pd.read_csv(COURSE / "DATA/continuation_repair_candidates_v1_1.csv")
        audit = pd.read_csv(COURSE / "DATA/stockfish_v1_1_candidate_500k.csv")
        self.assertEqual(cand["source_line_id"].tolist(), expected_source_ids)
        for row in cand[cand["editorial_decision"] == "REPAIR_CONTINUATION"].to_dict("records"):
            repair = repairs[(repairs["line_id"] == row["source_line_id"]) & (repairs["replacement_move_uci"] == row["repair_replacement_uci"])]
            self.assertFalse(repair.empty, row["source_line_id"])
            self.assertEqual(fen4(repair.iloc[0]["failure_fen"]), fen4(row["repair_fen"]))
        max_rows = audit.sort_values(["line_id", "loss_for_black_cp", "ply"], ascending=[True, False, True]).drop_duplicates("line_id").set_index("line_id")
        self.assertFalse((audit["loss_for_black_cp"].astype(int) > 25).any())
        games = list(parse_pgn_games(COURSE / "PGN/99_cours_v1_1_candidate.pgn"))
        self.assertEqual(len(games), 20)
        for game in games:
            line_id = game.headers.get("Round")
            self.assertNotIn("BILAN V1.1", game.comment or "")
            comments = []
            last = game
            for node in game.mainline():
                if node.comment:
                    comments.append((node, node.comment))
                last = node
            all_comments = "\n".join(comment for _, comment in comments)
            self.assertNotIn("BILAN — Ligne", all_comments)
            self.assertNotIn("Audit moteur des coups imposés", all_comments)
            self.assertNotIn("perte maximale observée", all_comments)
            bilans = [(node, comment) for node, comment in comments if "BILAN V1.1 —" in comment]
            self.assertEqual(len(bilans), 1, line_id)
            self.assertIs(bilans[0][0], last, line_id)
            row = max_rows.loc[line_id]
            expected_head = f"BILAN V1.1 — Coup noir maximal : {int(row['loss_for_black_cp'])} cp. Gate : PASS."
            self.assertIn(expected_head, bilans[0][1], line_id)
            if int(row["loss_for_black_cp"]) > 15:
                expected_tail = f"Maximum au ply {int(row['ply'])} sur ...{row['move_san']}."
                self.assertIn(expected_tail, bilans[0][1], (line_id, row["move_uci"]))
            else:
                self.assertNotIn("Maximum au ply", bilans[0][1], line_id)
        script_text = (COURSE / "LAB/scripts/propose_continuation_repairs.py").read_text(encoding="utf-8")
        self.assertNotIn("selected_ids = selected_ids[:22]", script_text)
        self.assertFalse((cand["source_line_id"] == pd.read_csv(COURSE / "DATA/core_40_index.csv")["line_id"].head(len(cand)).tolist()).all())
        family_share = cand["concept_family_id"].value_counts().max() / len(cand)
        self.assertLessEqual(family_share, 0.5)
        multi_non_london = cand[cand["system_group"] != "LONDON"].groupby("system_group").size()
        self.assertGreaterEqual(int((multi_non_london >= 2).sum()), 2)
        self.assertGreaterEqual((cand["system_group"] == "COLLE_ZUKERTORT").sum(), 2)
        self.assertGreaterEqual((cand["system_group"] == "JOBAVA").sum(), 2)
        self.assertGreaterEqual((cand["system_group"] == "TORRE").sum(), 2)
        self.assertGreaterEqual((cand["system_group"] == "VERESOV_PSEUDO_TROMP").sum(), 2)

    def test_v11_gpu_observed_only_summary_and_report_text(self):
        summary = json.loads((COURSE / "DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess_summary.json").read_text(encoding="utf-8"))
        detail = pd.read_csv(COURSE / "DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess.csv")
        observed = detail[detail["lichess_total"].fillna(0).astype(int) > 0]
        observed = observed[~((observed["speed"].astype(str) == "ALL") & (observed["missing_side"].astype(str) == "lichess"))]
        self.assertEqual(summary["lichess_observed_groups"], len(observed))
        self.assertEqual(summary["model_only_groups"], int((detail["elo"].astype(int) == 2100).sum()))
        self.assertEqual(summary["by_elo_observed_only"]["2100"]["status"], "MODEL_ONLY_NO_MATCHING_LICHESS_BAND")
        self.assertEqual(summary["by_elo_observed_only"]["2100"]["true_disagreements_observed_only"], 0)
        self.assertAlmostEqual(summary["top3_agreement_observed_only"], float(observed["top3_agreement"].fillna(False).astype(bool).mean()))
        self.assertNotEqual(summary["top3_agreement_observed_only"], 0.17916666666666667)
        decisions = pd.read_csv(COURSE / "DATA/editorial_line_decisions_v1_1.csv")
        self.assertNotIn("gpu_full_policy_groups_observed", decisions.columns)
        self.assertNotIn("gpu_top3_agreement_rate", decisions.columns)
        self.assertIn("gpu_maia_groups_total", decisions.columns)
        self.assertIn("gpu_lichess_observed_groups", decisions.columns)
        self.assertIn("gpu_top3_agreement_observed_only", decisions.columns)
        bdg_reason = decisions.loc[decisions["line_id"] == "BDG-01", "decision_reason"].iloc[0]
        self.assertNotIn("Continuation REJECT", bdg_reason)
        report = (COURSE / "PRODUCTION/RAPPORT_REFONTE_EDITORIALE_V1_1.md").read_text(encoding="utf-8")
        self.assertNotIn("0.17916666666666667", report)
        self.assertNotIn("doit être réaudité", report)
        self.assertIn("groupes Lichess observés : 72", report)
        self.assertIn("Les groupes sans données Lichess sont exclus", report)
        self.assertIn("Le PGN candidat a été réaudité à 500 000 nœuds : 215 coups noirs, 0 REVIEW, 0 REJECT, gate global PASS.", report)

    def test_v11_protected_v1_files_untouched(self):
        result = subprocess.run(
            ["git", "diff", "--name-only", "--", "brisez_les_systemes_v1/PGN/99_cours_v1_core_40.pgn", "brisez_les_systemes_v1/MANUSCRIT_COURS_V1.md"],
            cwd=COURSE.parent,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), "")


class CourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest(COURSE/"DATA/core_40_index.csv")
        cls.core_ids = set(cls.manifest["line_id"])

    def test_core_course(self):
        report=validate(COURSE/"PGN/99_cours_v1_core_40.pgn", COURSE/"DATA/core_40_index.csv")
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["games"],40)

    def test_manifest_key_moves_are_legal(self):
        for rec in self.manifest.to_dict("records"):
            board=chess.Board(rec["fen_before_key_move"]+" 0 1")
            move=chess.Move.from_uci(rec["key_move_uci"])
            self.assertIn(move,board.legal_moves,rec["line_id"])
            board.push(move)
            self.assertEqual(fen4(board),fen4(rec["fen_after_key_move"]),rec["line_id"])

    def test_essential_track(self):
        games=list(parse_pgn_games(COURSE/"PGN/00_parcours_essentiel_20.pgn"))
        ids=[g.headers.get("Round") for g in games]
        self.assertEqual(len(ids),20)
        self.assertEqual(len(set(ids)),20)
        self.assertTrue(set(ids) <= self.core_ids)

    def test_bias_chapters(self):
        files=sorted(p for p in (COURSE/"PGN").glob("0[1-8]_*.pgn"))
        self.assertEqual(len(files),8)
        union=set()
        for index,path in enumerate(files,start=1):
            games=list(parse_pgn_games(path))
            self.assertEqual(len(games),5,path.name)
            ids={g.headers.get("Round") for g in games}
            self.assertEqual(len(ids),5,path.name)
            for game in games:
                self.assertEqual(game.headers.get("BiasCode"),f"B{index}")
            union |= ids
        self.assertEqual(union,self.core_ids)

    def test_library_is_legal_and_unique(self):
        ids=[]
        for game in parse_pgn_games(COURSE/"PGN/90_bibliotheque_v0_9_88_lignes.pgn"):
            ids.append(game.headers.get("Round"))
            board=game.board()
            for move in game.mainline_moves():
                self.assertIn(move,board.legal_moves)
                board.push(move)
        self.assertEqual(len(ids),88)
        self.assertEqual(len(set(ids)),88)

    def test_rc1_has_no_unearned_composite_score(self):
        df=pd.read_csv(COURSE/"DATA/scorecards_core_40_rc1.csv")
        self.assertEqual(len(df),40)
        self.assertFalse(df["practical_edge_score_0_100"].notna().any())
        self.assertTrue((df["promotion_status"] == "INSUFFICIENT_EVIDENCE").all())


if __name__ == "__main__":
    unittest.main(verbosity=2)
