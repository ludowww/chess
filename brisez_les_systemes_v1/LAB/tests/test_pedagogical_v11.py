from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT.parent
sys.path.insert(0, str(ROOT / "scripts"))

from common import parse_pgn_games  # noqa: E402


class PedagogicalV11Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.player_path = COURSE / "PGN/00_parcours_essentiel_v1_1.pgn"
        cls.tech_path = COURSE / "PGN/99_cours_v1_1_candidate.pgn"
        cls.manifest_path = COURSE / "DATA/core_v1_1_pedagogical_manifest.csv"
        cls.report_path = COURSE / "PRODUCTION/RAPPORT_REVUE_PEDAGOGIQUE_V1_1.md"
        cls.player = list(parse_pgn_games(cls.player_path))
        cls.tech = {g.headers.get("SourceLineID"): g for g in parse_pgn_games(cls.tech_path)}
        cls.manifest = pd.read_csv(cls.manifest_path)

    def test_artifacts_composition_and_order(self):
        expected = [
            "ORD-01", "ORD-02", "COL-01", "VER-01", "COL-10",
            "LON-02", "LON-04", "LON-09",
            "LON-01", "LON-05", "LON-03",
            "PST-04", "LON-12",
            "PST-01", "TOR-02", "TOR-05", "LON-07",
            "JOB-09", "JOB-04", "TOR-06",
        ]
        self.assertTrue(self.player_path.exists())
        self.assertTrue(self.manifest_path.exists())
        self.assertTrue(self.report_path.exists())
        self.assertEqual(len(self.player), 20)
        self.assertEqual(self.manifest["source_line_id"].tolist(), expected)
        self.assertEqual([g.headers.get("SourceLineID") for g in self.player], expected)
        self.assertEqual(self.manifest["course_order"].tolist(), list(range(1, 21)))
        candidate = pd.read_csv(COURSE / "DATA/core_v1_1_candidate_manifest.csv")
        self.assertEqual(set(expected), set(candidate["source_line_id"]))
        bias_rank = {"B1": 1, "B2": 2, "B3": 3, "B4": 4, "B5": 5, "B7": 7, "B8": 8}
        ranks = [bias_rank[x] for x in self.manifest["bias_code"]]
        self.assertEqual(ranks, sorted(ranks))

    def test_each_player_line_is_exact_technical_prefix_and_stops_after_black(self):
        by_source = self.manifest.set_index("source_line_id")
        for game in self.player:
            source = game.headers.get("SourceLineID")
            self.assertIn(source, self.tech)
            player_moves = [m.uci() for m in game.mainline_moves()]
            tech_moves = [m.uci() for m in self.tech[source].mainline_moves()]
            self.assertEqual(player_moves, tech_moves[: len(player_moves)], source)
            self.assertEqual(len(player_moves) % 2, 0, source)
            self.assertEqual(len(player_moves), int(by_source.loc[source, "trainer_stop_ply"]), source)

    def test_headers_manifest_titles_moves_and_comments_align(self):
        by_source = self.manifest.set_index("source_line_id")
        comments_seen = set()
        for game in self.player:
            source = game.headers.get("SourceLineID")
            row = by_source.loc[source]
            self.assertEqual(game.headers.get("Round"), row["lesson_id"])
            self.assertEqual(game.headers.get("BiasCode"), row["bias_code"])
            self.assertEqual(game.headers.get("Chapter"), row["chapter_title"])
            self.assertEqual(game.headers.get("OpeningFamily"), row["opening_family"])
            self.assertEqual(game.headers.get("Tier"), row["tier"])
            self.assertEqual(game.headers.get("LessonMove"), row["lesson_move_san"])
            san_token = re.sub(r"[+#]$", "", str(row["lesson_move_san"]))
            coherence = " ".join([str(row["player_title"]), str(row["lesson_goal"])])
            lesson_comments = []
            for node in game.mainline():
                if node.move.uci() == row["lesson_move_uci"]:
                    lesson_comments.append(node.comment)
            self.assertEqual(len(lesson_comments), 1, source)
            comment = lesson_comments[0]
            self.assertIn(san_token, coherence + " " + comment, source)
            for label in ["Idée :", "Pourquoi :", "Suite :", "Mémo :"]:
                self.assertIn(label, comment, source)
            self.assertLessEqual(len(comment.split()), 90, source)
            self.assertNotIn(comment, comments_seen, source)
            comments_seen.add(comment)

    def test_no_laboratory_language_and_pst04_fact_is_correct(self):
        text = self.player_path.read_text(encoding="utf-8")
        forbidden = [
            "Réparation V1.1", "BILAN V1.1", "Gate : PASS", "centipions",
            "Stockfish", " FEN ", "audit moteur", "concept conservé",
        ]
        for term in forbidden:
            self.assertNotIn(term, text)
        pst = next(g for g in self.player if g.headers.get("SourceLineID") == "PST-04")
        comments = "\n".join(node.comment for node in pst.mainline() if node.comment)
        self.assertNotIn("deux pions", comments.lower())
        self.assertIn("un pion ne vaut pas un fou", comments.lower())

    def test_report_documents_b6_gap_and_protected_files_remain_separate(self):
        report = self.report_path.read_text(encoding="utf-8")
        self.assertIn("## B6 gap review", report)
        self.assertIn("BDG-01", report)
        self.assertIn("LON-09", report)
        self.assertIn("LON-05", report)
        self.assertIn("Tester `BDG-01`", report)
        self.assertNotEqual(self.player_path.read_text(encoding="utf-8"), self.tech_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
