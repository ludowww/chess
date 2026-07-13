from __future__ import annotations

import argparse
import csv
import io
import math
from collections import Counter
from pathlib import Path

import chess
import chess.engine
import chess.pgn
import pandas as pd

from common import fen4, parse_pgn_games, score_cp

FAMILY_RULES = [
    ("JOB", "JOBAVA_CENTER_BREAK", "Jobava : rupture centrale et cases noires"),
    ("VER", "VERESOV_CENTER_BREAK", "Veresov : rupture centrale et développement sobre"),
    ("TOR", "TORRE_E4_BISHOP_PRESSURE", "Torre : pression sur e4 et question au fou"),
    ("COL", "COLLE_LIGHT_SQUARE_DEVELOPMENT", "Colle/Zukertort : développement et cases centrales"),
    ("LON", "LONDON_QB6_DOUBLE_PRESSURE", "Londres : ...Qb6, d4 et b2 sous pression"),
    ("ORD", "LONDON_QB6_DOUBLE_PRESSURE", "Londres : ordres de coups et double pression"),
    ("EAR", "EARLY_WING_PAWN_CENTER_RESPONSE", "Aile précoce : répondre au centre"),
    ("BDG", "VERESOV_CENTER_BREAK", "Gambit/Veresov : accepter ou rendre au bon moment"),
]


def fen6(fen: str) -> str:
    parts = fen.split()
    if len(parts) == 4:
        return fen + " 0 1"
    if len(parts) == 6:
        return fen
    raise ValueError(f"Invalid FEN: {fen!r}")


def san_or_empty(board: chess.Board, uci: str) -> str:
    if not uci or (isinstance(uci, float) and math.isnan(uci)):
        return ""
    move = chess.Move.from_uci(str(uci))
    return board.san(move) if move in board.legal_moves else ""


def pv_san(board: chess.Board, moves: list[chess.Move]) -> str:
    b = board.copy(stack=False)
    out: list[str] = []
    for move in moves:
        if move not in b.legal_moves:
            break
        out.append(b.san(move))
        b.push(move)
    return " ".join(out)


def loss_gate(loss: int) -> str:
    if loss <= 25:
        return "PASS"
    if loss <= 50:
        return "REVIEW"
    return "REJECT"


def family_for(line_id: str) -> tuple[str, str]:
    for prefix, fam, title in FAMILY_RULES:
        if str(line_id).startswith(prefix):
            return fam, title
    return "SECONDARY_SYSTEM_CENTER_RESPONSE", "Systèmes secondaires : répondre au centre"


def best_replacements(engine: chess.engine.SimpleEngine, board: chess.Board, nodes: int, multipv: int = 4) -> list[dict]:
    infos = engine.analyse(board, chess.engine.Limit(nodes=nodes), multipv=multipv)
    if isinstance(infos, dict):
        infos = [infos]
    infos = sorted(infos, key=lambda x: x.get("multipv", 1))
    best_eval = score_cp(infos[0], board.turn)
    rows = []
    for info in infos:
        pv = info.get("pv", [])
        if not pv:
            continue
        move = pv[0]
        cand_eval = score_cp(info, board.turn)
        rows.append({
            "rank": int(info.get("multipv", len(rows) + 1)),
            "move": move,
            "move_uci": move.uci(),
            "move_san": board.san(move),
            "loss_cp": max(0, best_eval - cand_eval),
            "eval_cp": cand_eval,
            "pv": pv,
            "pv_uci": " ".join(m.uci() for m in pv[:8]),
            "pv_san": pv_san(board, pv[:8]),
        })
    return rows


def short_engine_line(engine: chess.engine.SimpleEngine, board: chess.Board, first: chess.Move, nodes: int, plies: int = 5) -> list[chess.Move]:
    b = board.copy(stack=False)
    line = []
    if first not in b.legal_moves:
        return line
    b.push(first); line.append(first)
    for _ in range(plies - 1):
        if b.is_game_over():
            break
        info = engine.analyse(b, chess.engine.Limit(nodes=max(80000, nodes // 6)))
        pv = info.get("pv", [])
        if not pv or pv[0] not in b.legal_moves:
            break
        b.push(pv[0]); line.append(pv[0])
    return line


def locate_failures(manifest: pd.DataFrame, stockfish: pd.DataFrame, key: pd.DataFrame, engine: chess.engine.SimpleEngine, nodes: int) -> pd.DataFrame:
    key_by_id = key.set_index("line_id")
    rows = []
    for rec in manifest.to_dict("records"):
        line_id = rec["line_id"]
        sf = stockfish[stockfish["line_id"] == line_id].copy()
        sf["loss_for_black_cp"] = sf["loss_for_black_cp"].astype(int)
        max_row = sf.sort_values(["loss_for_black_cp", "ply"], ascending=[False, True]).iloc[0]
        over25 = sf[(sf["loss_for_black_cp"] > 25) & (sf["move_uci"] != rec["key_move_uci"])]
        over50 = sf[(sf["loss_for_black_cp"] > 50) & (sf["move_uci"] != rec["key_move_uci"])]
        first25 = over25.sort_values("ply").iloc[0] if not over25.empty else None
        first50 = over50.sort_values("ply").iloc[0] if not over50.empty else None
        key_gate = key_by_id.loc[line_id, "key_move_gate"]
        key_loss = int(key_by_id.loc[line_id, "key_move_loss_cp"])
        if key_gate in {"REVIEW", "REJECT"}:
            failure_type = "KEY_MOVE_FAILURE"
            failure_fen = rec["fen_before_key_move"]
            original_move = rec["key_move_uci"]
        elif first50 is not None:
            failure_type = "LATER_CONTINUATION_REJECT"
            failure_fen = first50["fen_before"]
            original_move = first50["move_uci"]
        elif first25 is not None:
            failure_type = "LATER_CONTINUATION_REVIEW"
            failure_fen = first25["fen_before"]
            original_move = first25["move_uci"]
        else:
            failure_type = "NO_ENGINE_FAILURE"
            failure_fen = ""
            original_move = ""
        replacement = {"move_uci": "", "move_san": "", "loss_cp": ""}
        if failure_fen:
            board = chess.Board(fen6(str(failure_fen)))
            reps = best_replacements(engine, board, nodes=nodes, multipv=3)
            if reps:
                replacement = reps[0]
        rows.append({
            "line_id": line_id,
            "key_move_gate": key_gate,
            "key_move_loss_cp": key_loss,
            "line_max_loss_cp": int(max_row["loss_for_black_cp"]),
            "line_max_loss_ply": int(max_row["ply"]),
            "first_black_ply_over_25": "" if first25 is None else int(first25["ply"]),
            "first_black_move_over_25": "" if first25 is None else first25["move_uci"],
            "first_black_loss_over_25": "" if first25 is None else int(first25["loss_for_black_cp"]),
            "first_black_ply_over_50": "" if first50 is None else int(first50["ply"]),
            "first_black_move_over_50": "" if first50 is None else first50["move_uci"],
            "first_black_loss_over_50": "" if first50 is None else int(first50["loss_for_black_cp"]),
            "failure_fen": failure_fen,
            "best_replacement_uci": replacement["move_uci"],
            "best_replacement_san": replacement["move_san"],
            "replacement_loss_cp": replacement["loss_cp"],
            "failure_type": failure_type,
        })
    return pd.DataFrame(rows)


def write_repairs(manifest: pd.DataFrame, failures: pd.DataFrame, engine: chess.engine.SimpleEngine, nodes: int, output: Path) -> pd.DataFrame:
    manifest_by_id = manifest.set_index("line_id")
    rows = []
    for fail in failures.to_dict("records"):
        if fail["failure_type"] == "NO_ENGINE_FAILURE":
            continue
        rec = manifest_by_id.loc[fail["line_id"]].to_dict()
        board = chess.Board(fen6(str(fail["failure_fen"])))
        original_move = fail["first_black_move_over_50"] or fail["first_black_move_over_25"] or rec["key_move_uci"]
        original_san = san_or_empty(board, original_move)
        alternatives = best_replacements(engine, board, nodes=nodes, multipv=4)
        if original_move:
            alternatives = [a for a in alternatives if a["move_uci"] != original_move]
        for alt in alternatives[:3]:
            cont = short_engine_line(engine, board, alt["move"], nodes=nodes, plies=6)
            concept_preserved = "YES" if alt["loss_cp"] <= 25 and fail["failure_type"] != "KEY_MOVE_FAILURE" else "PARTIAL" if alt["loss_cp"] <= 50 else "NO"
            complexity = "SIMPLE" if len(cont) <= 4 and alt["loss_cp"] <= 25 else "MODERATE" if alt["loss_cp"] <= 50 else "COMPLEX"
            if concept_preserved == "YES" and complexity == "SIMPLE":
                reco = "KEEP_REPAIRED"
            elif fail["failure_type"] == "KEY_MOVE_FAILURE" and alt["loss_cp"] <= 50:
                reco = "REPLACE_KEY_MOVE"
            elif alt["loss_cp"] <= 50:
                reco = "SIDELINE_ONLY"
            else:
                reco = "DROP"
            rows.append({
                "line_id": fail["line_id"],
                "original_title": rec.get("title", ""),
                "original_concept": rec.get("concept", ""),
                "failure_type": fail["failure_type"],
                "failure_ply": fail["first_black_ply_over_50"] or fail["first_black_ply_over_25"] or "key",
                "failure_fen": fail["failure_fen"],
                "original_move_uci": original_move,
                "original_move_san": original_san,
                "original_loss_cp": fail["first_black_loss_over_50"] or fail["first_black_loss_over_25"] or fail["key_move_loss_cp"],
                "replacement_rank": alt["rank"],
                "replacement_move_uci": alt["move_uci"],
                "replacement_move_san": alt["move_san"],
                "replacement_loss_cp": alt["loss_cp"],
                "resulting_eval_cp": alt["eval_cp"],
                "candidate_continuation_uci": " ".join(m.uci() for m in cont),
                "candidate_continuation_san": pv_san(board, cont),
                "concept_preserved": concept_preserved,
                "repair_complexity": complexity,
                "technical_recommendation": reco,
                "human_explanation_hint": f"Remplacer {original_san or original_move} par {alt['move_san']} si le même plan reste lisible; vérifier pédagogiquement la mémorisation.",
            })
    df = pd.DataFrame(rows)
    df.to_csv(output, index=False)
    return df


def classify(manifest: pd.DataFrame, key: pd.DataFrame, failures: pd.DataFrame, repairs: pd.DataFrame, gpu_summary: dict | None, output: Path) -> pd.DataFrame:
    rows = []
    repair_simple = set(repairs[(repairs["technical_recommendation"] == "KEEP_REPAIRED") & (repairs["repair_complexity"] == "SIMPLE")]["line_id"]) if not repairs.empty else set()
    replacement_ok = set(repairs[repairs["technical_recommendation"].isin(["REPLACE_KEY_MOVE", "KEEP_REPAIRED"])] ["line_id"]) if not repairs.empty else set()
    key_by_id = key.set_index("line_id")
    fail_by_id = failures.set_index("line_id")
    for rec in manifest.to_dict("records"):
        line_id = rec["line_id"]
        key_gate = key_by_id.loc[line_id, "key_move_gate"]
        failure_type = fail_by_id.loc[line_id, "failure_type"]
        line_max = int(fail_by_id.loc[line_id, "line_max_loss_cp"])
        fam, fam_title = family_for(line_id)
        maia = rec.get("maia3_status", "") or rec.get("maia_status", "")
        lichess = rec.get("lichess_status", "") or rec.get("lichess_exact_position_status", "")
        if key_gate == "REJECT":
            decision = "REPLACE_KEY_MOVE" if line_id in replacement_ok else "DROP"
            reason = "Coup-clé objectivement trop coûteux; remplacement seulement si une alternative conserve le plan."
        elif key_gate == "REVIEW":
            decision = "REPLACE_KEY_MOVE" if line_id in replacement_ok else "SIDELINE_ONLY"
            reason = "Coup-clé jouable mais assez imprécis: garder hors noyau sauf remplacement très simple."
        elif failure_type == "LATER_CONTINUATION_REJECT":
            decision = "REPAIR_CONTINUATION" if line_id in repair_simple else "SIDELINE_ONLY"
            reason = "Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central."
        elif failure_type == "LATER_CONTINUATION_REVIEW":
            decision = "REPAIR_CONTINUATION" if line_id in repair_simple else "KEEP_CORE"
            reason = "Défaut ultérieur modéré; concept transférable si la continuation est clarifiée."
        else:
            decision = "KEEP_CORE" if line_max <= 50 else "SIDELINE_ONLY"
            reason = "Coup-clé sain et pas de défaut moteur critique dans la ligne principale."
        original_engine_gate = loss_gate(line_max)
        rows.append({
            "line_id": line_id,
            "original_engine_gate": original_engine_gate,
            "key_move_gate": key_gate,
            "failure_type": failure_type,
            "maia_status": maia,
            "lichess_exact_position_status": lichess,
            "concept_family_id": fam,
            "concept_family_title": fam_title,
            "decision": decision,
            "decision_reason": reason,
            "candidate_replacement_id": "" if line_id not in set(repairs.get("line_id", [])) else f"{line_id}-R1",
            "candidate_core_priority": "A" if decision in {"KEEP_CORE", "REPAIR_CONTINUATION"} else "B" if decision == "SIDELINE_ONLY" else "C",
        })
    df = pd.DataFrame(rows)
    df.to_csv(output, index=False)
    return df


def clone_prefix_until(game: chess.pgn.Game, stop_fen: str | None = None) -> tuple[chess.pgn.Game, chess.Board, chess.pgn.ChildNode]:
    new = chess.pgn.Game()
    for k, v in game.headers.items():
        new.headers[k] = v
    b = game.board()
    node = new
    for old_node in game.mainline():
        if stop_fen and fen4(b) == fen4(stop_fen):
            break
        san = b.san(old_node.move)
        node = node.add_variation(old_node.move)
        node.comment = old_node.comment
        b.push(old_node.move)
    return new, b, node


def build_candidate(manifest: pd.DataFrame, decisions: pd.DataFrame, failures: pd.DataFrame, repairs: pd.DataFrame, pgn_path: Path, out_pgn: Path, out_manifest: Path) -> pd.DataFrame:
    games_by_id = {g.headers.get("Round"): g for g in parse_pgn_games(pgn_path)}
    dec_by_id = decisions.set_index("line_id")
    fail_by_id = failures.set_index("line_id")
    key_by_source = manifest.set_index("line_id")
    selected_ids = decisions[decisions["decision"].isin(["KEEP_CORE", "REPAIR_CONTINUATION"])] ["line_id"].tolist()
    # Keep 22 lines when possible, preserving manifest order and broad coverage.
    if len(selected_ids) < 20:
        selected_ids += decisions[decisions["decision"] == "SIDELINE_ONLY"]["line_id"].tolist()
    selected_ids = selected_ids[:22]
    rows = []
    exported = []
    repair_first = repairs.sort_values(["line_id", "replacement_rank"]).drop_duplicates("line_id") if not repairs.empty else pd.DataFrame()
    repair_by_id = repair_first.set_index("line_id") if not repair_first.empty else None
    for order, source_id in enumerate(selected_ids, 1):
        rec = key_by_source.loc[source_id].to_dict()
        game = games_by_id[source_id]
        decision = dec_by_id.loc[source_id]
        failure = fail_by_id.loc[source_id]
        line_id_v11 = f"V11-{order:02d}-{source_id}"
        if decision["decision"] == "REPAIR_CONTINUATION" and repair_by_id is not None and source_id in repair_by_id.index:
            rep = repair_by_id.loc[source_id]
            new_game, board, node = clone_prefix_until(game, str(rep["failure_fen"]))
            for uci in str(rep["candidate_continuation_uci"]).split():
                mv = chess.Move.from_uci(uci)
                if mv not in board.legal_moves:
                    break
                node = node.add_variation(mv)
                node.comment = "Réparation V1.1 : alternative simple proposée par Stockfish, à retenir comme plan sobre."
                board.push(mv)
        else:
            new_game, board, node = clone_prefix_until(game, None)
        new_game.headers["Event"] = f"V1.1 candidat / {rec.get('chapter_opening','')} / {rec.get('title','')}"
        new_game.headers["Round"] = line_id_v11
        new_game.headers["SourceLineID"] = source_id
        new_game.headers["CourseRole"] = "CORE_V1_1_CANDIDATE"
        new_game.headers["Version"] = "1.1-candidate"
        exported.append(new_game)
        fam, fam_title = family_for(source_id)
        rows.append({
            "core_order": order,
            "line_id_v1_1": line_id_v11,
            "source_line_id": source_id,
            "bias_code": rec.get("bias_code", ""),
            "chapter_title": rec.get("chapter_opening", ""),
            "title": rec.get("title", ""),
            "tier": rec.get("tier", ""),
            "key_move_uci": rec.get("key_move_uci", ""),
            "key_move_san": rec.get("key_move_san", ""),
            "fixed_prefix": rec.get("fixed_prefix", ""),
            "fen_before_key_move": rec.get("fen_before_key_move", ""),
            "fen_after_key_move": rec.get("fen_after_key_move", ""),
            "concept": rec.get("concept", ""),
            "black_plan": rec.get("black_plan", ""),
            "memory_rule": rec.get("memory_rule", ""),
            "concept_family_id": fam,
            "concept_family_title": fam_title,
            "exact_position_role": "CORE" if decision["decision"] == "KEEP_CORE" else "REPAIRED_CORE",
            "key_move_gate": decision["key_move_gate"],
            "continuation_gate": failure["failure_type"],
            "editorial_decision": decision["decision"],
        })
    out_pgn.parent.mkdir(parents=True, exist_ok=True)
    with out_pgn.open("w", encoding="utf-8") as f:
        for g in exported:
            exporter = chess.pgn.StringExporter(headers=True, variations=False, comments=True)
            f.write(g.accept(exporter).strip() + "\n\n")
    cand = pd.DataFrame(rows)
    cand.to_csv(out_manifest, index=False)
    return cand


def write_report(manifest: pd.DataFrame, key: pd.DataFrame, failures: pd.DataFrame, decisions: pd.DataFrame, cand: pd.DataFrame, repairs: pd.DataFrame, out: Path) -> None:
    gate_counts = Counter(key["key_move_gate"])
    decision_counts = Counter(decisions["decision"])
    failure_counts = Counter(failures["failure_type"])
    lines = []
    lines.append("# Rapport refonte éditoriale V1.1\n")
    lines.append("## Synthèse\n")
    lines.append(f"- Taille V1 : 40 lignes.\n- Taille proposée V1.1 : {len(cand)} lignes.\n")
    for d in ["KEEP_CORE", "REPAIR_CONTINUATION", "REPLACE_KEY_MOVE", "SIDELINE_ONLY", "DROP"]:
        lines.append(f"- {d} : {decision_counts.get(d,0)}\n")
    lines.append("\nPreuve GPU utilisée uniquement comme confirmation méthodologique : CPU/GPU top 3 identique, top 1 Maia/Lichess observé environ 53 %, top 3 environ 91,5 %, top 10 environ 99,25 %. Ces chiffres ne sont pas interprétés comme fréquence réelle de jeu.\n")
    lines.append("\n## Distribution coup-clé\n")
    for g in ["PASS", "REVIEW", "REJECT"]:
        lines.append(f"- {g} : {gate_counts.get(g,0)}\n")
    lines.append("\n## Audit des 16 lignes précédemment PASS\n")
    pass_like = decisions[decisions["original_engine_gate"] == "PASS"]
    for row in pass_like.to_dict("records"):
        role = "reste dans le core" if row["line_id"] in set(cand["source_line_id"]) else "devient sideline (rareté/redondance)"
        lines.append(f"- {row['line_id']} : {row['decision']} — {role}. {row['decision_reason']}\n")
    lines.append("\n## Audit des 10 lignes REVIEW\n")
    for row in decisions[decisions["original_engine_gate"] == "REVIEW"].to_dict("records"):
        k = key[key["line_id"] == row["line_id"]].iloc[0]
        fail = failures[failures["line_id"] == row["line_id"]].iloc[0]
        repair = repairs[repairs["line_id"] == row["line_id"]].head(1)
        repair_text = "aucune réparation simple retenue" if repair.empty else f"réparation proposée: {repair.iloc[0]['replacement_move_san']} ({repair.iloc[0]['technical_recommendation']})"
        lines.append(f"- {row['line_id']} : coup-clé sain ({k['key_move_gate']}, {k['key_move_loss_cp']} cp) ; première imprécision {fail['failure_type']} ; {repair_text} ; décision {row['decision']}.\n")
    lines.append("\n## Audit des 14 lignes REJECT\n")
    for row in decisions[decisions["original_engine_gate"] == "REJECT"].to_dict("records"):
        k = key[key["line_id"] == row["line_id"]].iloc[0]
        fail = failures[failures["line_id"] == row["line_id"]].iloc[0]
        cause = "coup-clé réellement mauvais" if k["key_move_gate"] == "REJECT" else "coup-clé sain mais continuation ultérieure mauvaise"
        recover = "concept récupérable en sideline/réparation" if row["line_id"] in set(repairs.get("line_id", [])) else "concept à abandonner dans le cœur"
        lines.append(f"- {row['line_id']} : {cause} ; premier défaut {fail['failure_type']} ; {recover} ; décision {row['decision']}.\n")
    lines.append("\n## Noyau V1.1 proposé\n")
    for row in cand.to_dict("records"):
        lines.append(f"{row['core_order']}. {row['line_id_v1_1']} ← {row['source_line_id']} — {row['title']} ({row['editorial_decision']}, {row['concept_family_id']})\n")
    lines.append("\n## Sidelines\n")
    for row in decisions[decisions["decision"] == "SIDELINE_ONLY"].to_dict("records"):
        lines.append(f"- {row['line_id']} — {row['concept_family_title']} : {row['decision_reason']}\n")
    lines.append("\n## Familles\n")
    for fam, group in decisions.groupby("concept_family_id"):
        lines.append(f"- {fam} — {group.iloc[0]['concept_family_title']} : {len(group)} lignes, structure/objectif noir comparables ; réponse humaine et règle mémoire réutilisables.\n")
    lines.append("\n## Questions humaines restantes\n")
    lines.append("- La rareté exacte d'une position doit-elle sortir une ligne du MoveTrainer central malgré sa santé moteur ?\n")
    lines.append("- La réparation proposée est-elle mémorisable pour un joueur 1000–1800 ou seulement techniquement bonne ?\n")
    lines.append("- Certaines familles se recouvrent-elles trop dans l'expérience Chessable réelle ?\n")
    lines.append("- Le ton des commentaires conserve-t-il décision + plan + règle mémoire sans promesse commerciale excessive ?\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Locate continuation failures, propose repairs, and build V1.1 editorial candidate.")
    parser.add_argument("--manifest", default="DATA/core_40_index.csv")
    parser.add_argument("--stockfish", default="DATA/stockfish_v1_500k.csv")
    parser.add_argument("--key-audit", default="DATA/key_move_audit_v1_1.csv")
    parser.add_argument("--pgn", default="PGN/99_cours_v1_core_40.pgn")
    parser.add_argument("--engine", default="/usr/local/bin/stockfish18")
    parser.add_argument("--nodes", type=int, default=250000)
    args = parser.parse_args(argv)
    manifest = pd.read_csv(args.manifest)
    stockfish = pd.read_csv(args.stockfish)
    key = pd.read_csv(args.key_audit)
    with chess.engine.SimpleEngine.popen_uci(args.engine) as engine:
        engine.configure({"Threads": 2, "Hash": 512})
        failures = locate_failures(manifest, stockfish, key, engine, nodes=args.nodes)
        failures.to_csv("DATA/continuation_failure_audit_v1_1.csv", index=False)
        repairs = write_repairs(manifest, failures, engine, nodes=args.nodes, output=Path("DATA/continuation_repair_candidates_v1_1.csv"))
    decisions = classify(manifest, key, failures, repairs, None, Path("DATA/editorial_line_decisions_v1_1.csv"))
    cand = build_candidate(manifest, decisions, failures, repairs, Path(args.pgn), Path("PGN/99_cours_v1_1_candidate.pgn"), Path("DATA/core_v1_1_candidate_manifest.csv"))
    write_report(manifest, key, failures, decisions, cand, repairs, Path("PRODUCTION/RAPPORT_REFONTE_EDITORIALE_V1_1.md"))
    print(f"wrote failures={len(failures)} repairs={len(repairs)} decisions={len(decisions)} candidate={len(cand)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
