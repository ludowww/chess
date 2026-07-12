from __future__ import annotations

import sys
import unittest
from pathlib import Path

import chess
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT.parent
sys.path.insert(0, str(ROOT / "scripts"))

from common import elo_band, fen4, load_manifest, parse_pgn_games  # noqa: E402
from maia3_profile import (  # noqa: E402
    build_arg_parser,
    fen6,
    normalized_entropy,
    position_from_fixed_prefix,
    profile,
    set_position_from_record,
)
from compare_maia_profiles import compare_profiles  # noqa: E402
from compare_full_policy_lichess import compare_full_policy_to_lichess  # noqa: E402
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



class MaiaGpuToolingTests(unittest.TestCase):
    def test_amp_mode_parser_accepts_expected_values_and_rejects_invalid(self):
        parser = build_arg_parser()
        self.assertEqual(parser.parse_args(["--manifest", "m.csv", "--output", "o.csv", "--amp-mode", "auto"]).amp_mode, "auto")
        self.assertEqual(parser.parse_args(["--manifest", "m.csv", "--output", "o.csv", "--amp-mode", "on"]).amp_mode, "on")
        self.assertEqual(parser.parse_args(["--manifest", "m.csv", "--output", "o.csv", "--amp-mode", "off"]).amp_mode, "off")
        with self.assertRaises(SystemExit):
            parser.parse_args(["--manifest", "m.csv", "--output", "o.csv", "--amp-mode", "bad"])

    def test_profile_keeps_top10_default_and_exports_all_legal_policy_with_mass(self):
        import maia3_profile as mp

        class PolicyEngine(FakeMaiaEngine):
            def __init__(self, multipv):
                super().__init__()
                self.multipv = multipv
                self.self_elo = None
                self.oppo_elo = None

            def score_moves(self):
                legal = list(self.board.legal_moves)
                count = min(self.multipv, len(legal))
                p = 1.0 / count
                return legal[0], [
                    {"move": mv, "policy": p, "wdl": (500, 0, 500)}
                    for mv in legal[:count]
                ]

        manifest = pd.DataFrame([{
            "line_id": "TST-01",
            "bias_code": "B0",
            "fixed_prefix": "1. e4 e5",
            "fen_before_key_move": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -",
            "fen_after_key_move": chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2").fen(),
            "key_move_uci": "e7e5",
        }])
        tmp = COURSE / "DATA" / "GPU_LOCAL" / "unit_manifest.csv"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        manifest.to_csv(tmp, index=False)
        original = mp.load_direct_engine
        try:
            mp.load_direct_engine = lambda model, device, multipv, amp_mode="auto": PolicyEngine(multipv)
            top10 = profile(tmp, "maia3-79m", "cpu", [1100], 10)
            self.assertEqual(len(top10), 10)
            self.assertEqual(sorted(top10["rank"].tolist()), list(range(1, 11)))
            self.assertIn("amp_mode", top10.columns)
            full = profile(tmp, "maia3-79m", "cpu", [1100], 10, amp_mode="off", all_legal_moves=True)
            legal_count = chess.Board(manifest.iloc[0]["fen_after_key_move"]).legal_moves.count()
            self.assertEqual(len(full), legal_count)
            self.assertAlmostEqual(float(full["legal_policy_mass"].iloc[0]), 1.0, places=7)
        finally:
            mp.load_direct_engine = original
            tmp.unlink(missing_ok=True)

    def test_compare_maia_profiles_is_order_independent_and_reports_top_metrics(self):
        left = pd.DataFrame([
            {"line_id":"A", "elo":1100, "rank":1, "move_uci":"a2a3", "policy_probability":0.5, "fen":"8/8/8/8/8/8/P7/K6k w - -"},
            {"line_id":"A", "elo":1100, "rank":2, "move_uci":"a2a4", "policy_probability":0.5, "fen":"8/8/8/8/8/8/P7/K6k w - -"},
        ])
        right = left.iloc[[1,0]].copy()
        result = compare_profiles(left, right)
        self.assertEqual(result.summary["groups_left"], 1)
        self.assertEqual(result.summary["top1_agreement_rate"], 1.0)
        self.assertEqual(result.summary["top3_agreement_rate"], 1.0)
        self.assertEqual(result.summary["missing_groups"], 0)
        self.assertEqual(result.summary["fen_mismatches"], 0)

    def test_full_policy_lichess_comparison_expects_240_groups_and_detects_covered_mass(self):
        manifest = load_manifest(COURSE/"DATA/core_40_index.csv")[["line_id", "fen_after_key_move"]]
        maia_rows = []
        lichess_rows = []
        for line_id, fen in manifest.itertuples(index=False):
            for elo in [1100,1300,1500,1700,1900,2100]:
                maia_rows.append({"line_id":line_id,"elo":elo,"rank":1,"move_uci":"a2a3","policy_probability":0.6,"fen":fen})
                maia_rows.append({"line_id":line_id,"elo":elo,"rank":2,"move_uci":"a2a4","policy_probability":0.4,"fen":fen})
                lichess_rows.append({"line_id":line_id,"position_role":"after_key","elo_min":elo,"elo_max":elo+199,"speed":"blitz","split":"test","move_uci":"a2a3","count":3,"total_positions":5,"frequency":0.6})
                lichess_rows.append({"line_id":line_id,"position_role":"after_key","elo_min":elo,"elo_max":elo+199,"speed":"rapid","split":"test","move_uci":"a2a4","count":2,"total_positions":5,"frequency":0.4})
        detail, summary = compare_full_policy_to_lichess(pd.DataFrame(maia_rows), pd.DataFrame(lichess_rows), manifest)
        self.assertEqual(summary["expected_maia_groups"], 240)
        self.assertEqual(summary["maia_groups_observed"], 240)
        self.assertGreater(summary["overall_maia_mass_covered_by_lichess"], 0.99)
        self.assertIn("blitz", summary["by_speed"])
        self.assertFalse(detail.empty)

    def test_windows_scripts_present_and_repo_writes_stay_under_gpu_local(self):
        self.assertTrue((COURSE.parent/"tools/run_maia3_gpu_validation.ps1").exists())
        self.assertTrue((COURSE.parent/"tools/test_gpu_environment.ps1").exists())
        report = (COURSE.parent/"tools/run_maia3_gpu_validation.ps1").read_text(encoding="utf-8")
        self.assertIn("DATA/GPU_LOCAL", report.replace("\\", "/"))
        self.assertIn(".venv-gpu", report)
        self.assertNotIn("git commit", report.lower())
        self.assertNotIn("git push", report.lower())


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
