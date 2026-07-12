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
from maia3_profile import fen6, normalized_entropy, position_from_fixed_prefix, set_position_from_record  # noqa: E402
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
