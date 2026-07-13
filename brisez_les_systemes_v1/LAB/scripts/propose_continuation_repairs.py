from __future__ import annotations

import argparse
import csv
import io
import json
import math
from collections import Counter
from pathlib import Path

import chess
import chess.engine
import chess.pgn
import pandas as pd

from common import fen4, parse_pgn_games, score_cp

FAMILY_BY_LINE = {
    "ORD-01": ("LONDON_EARLY_C5_BG4", "Londres : ...c5 puis ...Bg4 sans sortie de dame"),
    "ORD-02": ("LONDON_QB6_DOUBLE_PRESSURE", "Londres : ...Qb6, d4 et b2 sous pression"),
    "ORD-09": ("EARLY_WING_PAWN_CENTER_RESPONSE", "Aile précoce : répondre au centre"),
    "ORD-10": ("LONDON_NH5_BISHOP_HUNT", "Londres : tempos h3/h4 et chasse du fou"),
    "LON-01": ("LONDON_QB3_C4_ENDGAME", "Londres : Qb3, ...c4 et finale axb6"),
    "LON-02": ("LONDON_QC1_CXD4_STRUCTURE", "Londres : dame blanche passive, centre clarifié"),
    "LON-03": ("LONDON_QB3_C4_ENDGAME", "Londres : Qb3, ...c4 et finale axb6"),
    "LON-04": ("LONDON_QC1_CXD4_STRUCTURE", "Londres : dame blanche passive, centre clarifié"),
    "LON-05": ("LONDON_QC1_CXD4_STRUCTURE", "Londres : dame blanche passive, centre clarifié"),
    "LON-06": ("LONDON_NH5_BISHOP_HUNT", "Londres : ...Nh5 et chasse du fou"),
    "LON-07": ("LONDON_NH5_BISHOP_HUNT", "Londres : ...Nh5/...h6/...g5 et chasse du fou"),
    "LON-09": ("LONDON_EARLY_C5_BG4", "Londres : développement sobre quand b2 est protégé"),
    "LON-10": ("LONDON_QB2_QUEEN_RAID", "Londres : raid de dame sur b2/c3"),
    "LON-11": ("LONDON_QB2_QUEEN_RAID", "Londres : raid de dame sur b2/c3"),
    "LON-12": ("LONDON_QB2_QUEEN_RAID", "Londres : raid de dame sur b2/c3"),
    "LON-15": ("LONDON_QB2_QUEEN_RAID", "Londres : raid de dame sur b2/c3"),
    "COL-01": ("COLLE_BF5_DEVELOPMENT", "Colle/Zukertort : sortir le fou avant e6"),
    "COL-10": ("COLLE_ZUKERTORT_C5_QC7", "Colle/Zukertort : ...c5 puis coordination ...Qc7"),
    "JOB-03": ("JOBAVA_DXC5_CENTER_BREAK", "Jobava : dxc5, rupture centrale"),
    "JOB-04": ("JOBAVA_NB5_CHECK_RESPONSE", "Jobava : Nb5+, développement et roi sûr"),
    "JOB-06": ("JOBAVA_F3_CENTER_BREAK", "Jobava : f3, ouvrir avant e4"),
    "JOB-09": ("JOBAVA_TEMPO_CENTER_BREAK", "Jobava : tempos d’aile, centre d’abord"),
    "JOB-10": ("JOBAVA_TEMPO_CENTER_BREAK", "Jobava : tempos d’aile, centre d’abord"),
    "JOB-11": ("JOBAVA_BXB8_ROOK_RECAPTURE", "Jobava : Bxb8 et activité de tour"),
    "JOB-12": ("JOBAVA_NB1_QB6_PRESSURE", "Jobava : retrait Nb1 et double pression"),
    "JOB-13": ("JOBAVA_PIN_QA5_MOTIF", "Jobava : clouage puis motif ...Qa5+"),
    "TOR-02": ("TORRE_H4_H5_BISHOP_TRAP", "Torre : ...h5 et restriction du fou"),
    "TOR-05": ("TORRE_H4_CENTER_RESPONSE", "Torre : h4, répondre par le centre"),
    "TOR-06": ("TORRE_NBD2_EXCHANGE_CENTER", "Torre : Nbd2, échange puis centre"),
    "TOR-08": ("TORRE_E3_F6_CENTER", "Torre : e3, ...f6-g5"),
    "TOR-09": ("TORRE_BISHOP_ROUTE_EXCHANGE", "Torre : route Bh4-h5-f6 et échange"),
    "TOR-10": ("TORRE_QB6_DOUBLE_PRESSURE", "Torre : ...Qb6, e4 et b2"),
    "VER-01": ("VERESOV_CENTER_BREAK", "Veresov : rupture centrale et développement sobre"),
    "VER-03": ("VERESOV_DXC5_CENTER_BREAK", "Veresov : dxc5, rendre par le centre"),
    "VER-05": ("VERESOV_GFILE_CENTER", "Veresov : structure gxf6 et centre"),
    "VER-08": ("VERESOV_F3_CENTER_BREAK", "Veresov : f3, ouvrir avant e4"),
    "PST-01": ("PSEUDO_TROMP_H6_CENTER", "Pseudo-Trompowsky : demander au fou puis centre"),
    "PST-04": ("PSEUDO_TROMP_BISHOP_SAC", "Pseudo-Trompowsky : sacrifice de fou insuffisant"),
    "STO-01": ("STONEWALL_C4_FIX", "Stonewall : fixer par ...c4"),
    "BDG-01": ("BDG_ACCEPT_AND_DEVELOP", "Blackmar-Diemer : accepter puis développer"),
}

MANDATORY_REPAIRS = {
    "ORD-01": "f7f6",
    "COL-10": "d8c7",
    "LON-04": "a8c8",
    "LON-03": "c8f5",
    "LON-07": "c8f5",
    "TOR-05": "d8b6",
}

PREFERRED_EXTRA_REPAIRS = {"TOR-06": "f8d6"}

CORE_SEED_IDS = [
    "ORD-01", "ORD-02", "COL-01", "COL-10", "VER-01", "LON-02", "LON-04", "LON-09",
    "LON-01", "LON-03", "LON-05", "JOB-09", "PST-04", "LON-12", "TOR-02", "PST-01",
    "BDG-01", "LON-07", "TOR-06", "LON-06", "ORD-09",
]


def fen6(fen: str) -> str:
    parts = fen.split()
    if len(parts) == 4:
        return fen + " 0 1"
    if len(parts) == 6:
        return fen
    raise ValueError(f"Invalid FEN: {fen!r}")


def family_for(line_id: str) -> tuple[str, str]:
    return FAMILY_BY_LINE.get(str(line_id), ("SECONDARY_SYSTEM_CENTER_RESPONSE", "Systèmes secondaires : répondre au centre"))


def system_group(line_id: str) -> str:
    if str(line_id).startswith(("LON", "ORD")):
        return "LONDON"
    if str(line_id).startswith("COL"):
        return "COLLE_ZUKERTORT"
    if str(line_id).startswith("JOB"):
        return "JOBAVA"
    if str(line_id).startswith("TOR"):
        return "TORRE"
    if str(line_id).startswith(("VER", "PST")):
        return "VERESOV_PSEUDO_TROMP"
    return "SECONDARY_GAMBIT_STONEWALL"


def loss_gate(loss: int) -> str:
    if loss <= 25:
        return "PASS"
    if loss <= 50:
        return "REVIEW"
    return "REJECT"


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
            if concept_preserved == "YES" and complexity in {"SIMPLE", "MODERATE"} and alt["loss_cp"] <= 25:
                reco = "KEEP_REPAIRED"
            elif fail["failure_type"] == "KEY_MOVE_FAILURE" and alt["loss_cp"] <= 25:
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


def _blank_to_none(value):
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if str(value).strip() == "":
        return None
    return value


def load_empirical_context(course_dir: Path) -> tuple[pd.DataFrame | None, dict | None, dict | None]:
    score_path = course_dir / "DATA/scorecards_validated_expanded_corrected.csv"
    validation_path = course_dir / "DATA/corrected_validation_summary.json"
    gpu_path = course_dir / "DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess_summary.json"
    scorecards = pd.read_csv(score_path) if score_path.exists() else None
    validation = json.loads(validation_path.read_text(encoding="utf-8")) if validation_path.exists() else None
    gpu = json.loads(gpu_path.read_text(encoding="utf-8")) if gpu_path.exists() else None
    return scorecards, validation, gpu


def classify(manifest: pd.DataFrame, key: pd.DataFrame, failures: pd.DataFrame, repairs: pd.DataFrame, gpu_summary: dict | None, output: Path) -> pd.DataFrame:
    rows = []
    ok_repairs = pd.DataFrame()
    if not repairs.empty:
        ok_repairs = repairs[
            (repairs["technical_recommendation"] == "KEEP_REPAIRED")
            & (repairs["concept_preserved"] == "YES")
            & (repairs["repair_complexity"].isin(["SIMPLE", "MODERATE"]))
            & (repairs["replacement_loss_cp"].astype(int) <= 25)
        ].copy()
    repair_ok = set(ok_repairs["line_id"]) if not ok_repairs.empty else set()
    forced_repairs = set(MANDATORY_REPAIRS) | set(PREFERRED_EXTRA_REPAIRS)
    key_by_id = key.set_index("line_id")
    fail_by_id = failures.set_index("line_id")
    scorecards, validation_summary, gpu_file_summary = load_empirical_context(Path.cwd())
    score_by_id = scorecards.set_index("line_id") if scorecards is not None else None
    gpu_used = gpu_summary or gpu_file_summary or {}

    for rec in manifest.to_dict("records"):
        line_id = rec["line_id"]
        key_gate = key_by_id.loc[line_id, "key_move_gate"]
        failure_type = fail_by_id.loc[line_id, "failure_type"]
        line_max = int(fail_by_id.loc[line_id, "line_max_loss_cp"])
        replacement_required = line_id in forced_repairs
        has_repair = line_id in repair_ok
        fam, fam_title = family_for(line_id)
        sc = score_by_id.loc[line_id].to_dict() if score_by_id is not None and line_id in score_by_id.index else {}
        empirical_total = int(sc.get("empirical_total_after_key", 0) or 0)
        empirical_gate = sc.get("empirical_sample_gate", "MISSING") or "MISSING"
        maia_status = sc.get("maia_status", rec.get("maia3_status", "MISSING")) or "MISSING"
        lichess_status = "OBSERVED" if empirical_total > 0 else "NO_EXACT_POSITION_SAMPLE"
        maia_proxy = sc.get("maia_human_error_proxy_0_100", "")
        practical_edge = sc.get("practical_edge_score_0_100", "")
        simplicity = int(rec.get("editorial_our_simplicity_1_5", 3) or 3)
        longevity = int(rec.get("editorial_learning_longevity_1_5", 3) or 3)
        redundant = system_group(line_id) == "LONDON" and line_id in {"LON-06", "ORD-09", "ORD-10", "LON-10", "LON-15"}
        rare = empirical_total < 10

        if key_gate != "PASS":
            decision = "SIDELINE_ONLY"
            reason = "Coup-clé non PASS : exclu du noyau V1.1."
        elif failure_type == "NO_ENGINE_FAILURE" and line_max <= 25:
            decision = "KEEP_CORE"
            reason = "Concept sain et variante naturellement PASS sur l'audit V1."
        elif failure_type == "LATER_CONTINUATION_REVIEW" and has_repair:
            decision = "REPAIR_CONTINUATION"
            reason = "Continuation REVIEW réparée par une alternative <=25 cp, concept conservé, complexité simple/modérée."
        elif failure_type == "LATER_CONTINUATION_REVIEW":
            decision = "SIDELINE_ONLY"
            reason = "Continuation REVIEW sans réparation assez simple validée : sideline."
        else:
            decision = "SIDELINE_ONLY"
            reason = "Continuation REJECT ou réparation insuffisante : hors noyau."

        if rare and decision == "KEEP_CORE" and line_id not in CORE_SEED_IDS:
            decision = "SIDELINE_ONLY"
            reason = "Concept sain mais échantillon empirique trop rare pour priorité core."
        if redundant and line_id not in CORE_SEED_IDS and decision == "KEEP_CORE":
            decision = "SIDELINE_ONLY"
            reason = "Concept sain mais redondant avec une famille Londres déjà couverte."

        engine_score = 100 if decision == "KEEP_CORE" else 90 if decision == "REPAIR_CONTINUATION" else 40
        selection_score = (
            engine_score
            + simplicity * 8
            + longevity * 8
            + (8 if maia_status == "AVAILABLE" else 0)
            + min(empirical_total, 100) / 5
            - (20 if redundant else 0)
            - (8 if rare else 0)
        )
        if line_id == "JOB-04":
            selection_score += 20
        if system_group(line_id) != "LONDON":
            selection_score += 10
        rows.append({
            "line_id": line_id,
            "original_engine_gate": loss_gate(line_max),
            "key_move_gate": key_gate,
            "failure_type": failure_type,
            "candidate_max_loss_cp_before_repair": line_max,
            "maia_status": maia_status,
            "lichess_exact_position_status": lichess_status,
            "empirical_total_after_key": empirical_total,
            "empirical_sample_gate": empirical_gate,
            "maia_human_error_proxy": maia_proxy,
            "practical_edge_score": practical_edge,
            "concept_family_id": fam,
            "concept_family_title": fam_title,
            "system_group": system_group(line_id),
            "decision": decision,
            "decision_reason": reason,
            "candidate_replacement_id": f"{line_id}-R1" if has_repair else "",
            "candidate_core_priority": "A" if line_id in CORE_SEED_IDS else "B" if decision in {"KEEP_CORE", "REPAIR_CONTINUATION"} else "C",
            "selection_score": round(selection_score, 3),
            "rarity_flag": "RARE" if rare else "OBSERVED",
            "redundancy_flag": "REDUNDANT" if redundant else "DISTINCT",
            "gpu_full_policy_groups_observed": gpu_used.get("maia_groups_observed", ""),
            "gpu_top3_agreement_rate": gpu_used.get("overall_top3_agreement_rate", ""),
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


def select_core_ids(decisions: pd.DataFrame) -> list[str]:
    eligible = decisions[decisions["decision"].isin(["KEEP_CORE", "REPAIR_CONTINUATION"])].copy()
    eligible["seed_rank"] = eligible["line_id"].map({line_id: i for i, line_id in enumerate(CORE_SEED_IDS)}).fillna(999).astype(int)
    selected: list[str] = []
    for line_id in CORE_SEED_IDS:
        row = eligible[eligible["line_id"] == line_id]
        if not row.empty:
            selected.append(line_id)
    if len(selected) < 20:
        for line_id in eligible.sort_values(["selection_score", "seed_rank"], ascending=[False, True])["line_id"]:
            if line_id not in selected:
                selected.append(line_id)
            if len(selected) >= 20:
                break
    selected = selected[:22]
    counts = Counter(system_group(x) for x in selected)
    if counts.get("LONDON", 0) > len(selected) // 2:
        non_selected_non_london = [
            line_id for line_id in eligible.sort_values("selection_score", ascending=False)["line_id"]
            if line_id not in selected and system_group(line_id) != "LONDON"
        ]
        for replacement in non_selected_non_london:
            london_candidates = [x for x in reversed(selected) if system_group(x) == "LONDON" and x not in MANDATORY_REPAIRS]
            if not london_candidates:
                break
            selected[selected.index(london_candidates[0])] = replacement
            counts = Counter(system_group(x) for x in selected)
            if counts.get("LONDON", 0) <= len(selected) // 2:
                break
    return selected


def clone_prefix_until(game: chess.pgn.Game, stop_fen: str | None = None) -> tuple[chess.pgn.Game, chess.Board, chess.pgn.ChildNode]:
    new = chess.pgn.Game()
    for k, v in game.headers.items():
        new.headers[k] = v
    b = game.board()
    node = new
    found = stop_fen is None
    for old_node in game.mainline():
        if stop_fen and fen4(b) == fen4(stop_fen):
            found = True
            break
        node = node.add_variation(old_node.move)
        node.comment = old_node.comment
        b.push(old_node.move)
    if stop_fen and not found:
        raise ValueError(f"Repair anchor not found in PGN mainline: {stop_fen}")
    return new, b, node


def _repair_table(repairs: pd.DataFrame) -> pd.DataFrame:
    if repairs.empty:
        return repairs
    ok = repairs[
        (repairs["technical_recommendation"] == "KEEP_REPAIRED")
        & (repairs["concept_preserved"] == "YES")
        & (repairs["repair_complexity"].isin(["SIMPLE", "MODERATE"]))
        & (repairs["replacement_loss_cp"].astype(int) <= 25)
    ].copy()
    forced = {**MANDATORY_REPAIRS, **PREFERRED_EXTRA_REPAIRS}
    ok["forced_rank"] = ok.apply(lambda r: 0 if forced.get(r["line_id"]) == r["replacement_move_uci"] else 1, axis=1)
    return ok.sort_values(["line_id", "forced_rank", "replacement_loss_cp", "replacement_rank"]).drop_duplicates("line_id")


def build_candidate(manifest: pd.DataFrame, decisions: pd.DataFrame, failures: pd.DataFrame, repairs: pd.DataFrame, pgn_path: Path, out_pgn: Path, out_manifest: Path) -> pd.DataFrame:
    games_by_id = {g.headers.get("Round"): g for g in parse_pgn_games(pgn_path)}
    dec_by_id = decisions.set_index("line_id")
    key_by_source = manifest.set_index("line_id")
    selected_ids = select_core_ids(decisions)
    rows = []
    exported = []
    repair_first = _repair_table(repairs)
    repair_by_id = repair_first.set_index("line_id") if not repair_first.empty else None
    for order, source_id in enumerate(selected_ids, 1):
        rec = key_by_source.loc[source_id].to_dict()
        game = games_by_id[source_id]
        decision = dec_by_id.loc[source_id]
        line_id_v11 = f"V11-{order:02d}-{source_id}"
        repair_move = ""
        repair_fen = ""
        repair_san = ""
        if decision["decision"] == "REPAIR_CONTINUATION":
            if repair_by_id is None or source_id not in repair_by_id.index:
                raise ValueError(f"Missing accepted repair for core line {source_id}")
            rep = repair_by_id.loc[source_id]
            repair_fen = str(rep["failure_fen"])
            repair_move = str(rep["replacement_move_uci"])
            repair_san = str(rep["replacement_move_san"])
            new_game, board, node = clone_prefix_until(game, repair_fen)
            san_parts = str(rep["candidate_continuation_san"])
            for index, uci in enumerate(str(rep["candidate_continuation_uci"]).split()):
                mv = chess.Move.from_uci(uci)
                if mv not in board.legal_moves:
                    raise ValueError(f"Illegal repair move {uci} for {source_id} at {board.fen()}")
                node = node.add_variation(mv)
                if index == 0:
                    node.comment = f"Réparation V1.1 : {repair_san} remplace la continuation initiale au même FEN. Plan sobre : développement, roi sûr, concept conservé."
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
            "line_id": line_id_v11,
            "line_id_v1_1": line_id_v11,
            "source_line_id": source_id,
            "bias_code": rec.get("bias_code", ""),
            "chapter_title": rec.get("chapter_opening", ""),
            "title": rec.get("title", ""),
            "tier": rec.get("tier", ""),
            "system_group": system_group(source_id),
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
            "continuation_gate": "PASS" if decision["decision"] == "KEEP_CORE" else "REPAIRED_PASS",
            "editorial_decision": decision["decision"],
            "repair_fen": repair_fen,
            "repair_replacement_uci": repair_move,
            "repair_replacement_san": repair_san,
            "selection_score": decision.get("selection_score", ""),
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
    decision_counts = Counter(decisions["decision"])
    family_counts = Counter(cand["concept_family_id"])
    system_counts = Counter(cand["system_group"])
    lines = []
    lines.append("# Rapport refonte éditoriale V1.1\n")
    lines.append("## Synthèse\n")
    lines.append(f"- Taille V1 : 40 lignes.\n- Taille noyau candidat V1.1 : {len(cand)} lignes.\n")
    for d in ["KEEP_CORE", "REPAIR_CONTINUATION", "REPLACE_KEY_MOVE", "SIDELINE_ONLY", "DROP"]:
        lines.append(f"- {d} : {decision_counts.get(d,0)}\n")
    lines.append("- Règle appliquée : KEEP_CORE seulement si coup-clé PASS, aucun défaut de continuation, et perte maximale <=25 cp.\n")
    lines.append("- Les continuations REVIEW/REJECT retenues dans le noyau passent par REPAIR_CONTINUATION avec remplacement <=25 cp, concept conservé, complexité SIMPLE/MODERATE.\n")

    lines.append("\n## Composition finale du core\n")
    for row in cand.to_dict("records"):
        repair = f" — réparation {row['repair_replacement_san']} au FEN exact" if row.get("repair_replacement_uci") else ""
        lines.append(f"{row['core_order']}. {row['line_id_v1_1']} ← {row['source_line_id']} — {row['title']} ({row['editorial_decision']}, {row['concept_family_id']}){repair}\n")

    repaired_ids = set(cand.loc[cand["editorial_decision"] == "REPAIR_CONTINUATION", "source_line_id"])
    natural_ids = set(cand.loc[cand["editorial_decision"] == "KEEP_CORE", "source_line_id"])
    lines.append("\n## Variantes naturellement PASS\n")
    for line_id in sorted(natural_ids):
        row = decisions[decisions["line_id"] == line_id].iloc[0]
        lines.append(f"- {line_id} — {row['concept_family_title']} ; max V1 avant candidat {row['candidate_max_loss_cp_before_repair']} cp.\n")
    lines.append("\n## Variantes réparées\n")
    for line_id in sorted(repaired_ids):
        rep = _repair_table(repairs)
        rr = rep[rep["line_id"] == line_id].iloc[0]
        lines.append(f"- {line_id} : {rr['original_move_san']} → {rr['replacement_move_san']} ({rr['replacement_move_uci']}), FEN {rr['failure_fen']}, perte réparation {rr['replacement_loss_cp']} cp, suite {rr['candidate_continuation_san']}.\n")

    lines.append("\n## Concepts sains sortis pour rareté / redondance / difficulté humaine\n")
    for reason_name, mask in [
        ("rareté", decisions["rarity_flag"] == "RARE"),
        ("redondance", decisions["redundancy_flag"] == "REDUNDANT"),
        ("difficulté humaine ou continuation non réparée", decisions["decision"] == "SIDELINE_ONLY"),
    ]:
        group = decisions[mask & ~decisions["line_id"].isin(set(cand["source_line_id"]))]
        lines.append(f"\n### Sorties pour {reason_name}\n")
        for row in group.to_dict("records"):
            lines.append(f"- {row['line_id']} — {row['concept_family_title']} : {row['decision_reason']} (Maia {row['maia_status']}, Lichess {row['lichess_exact_position_status']}, n={row['empirical_total_after_key']}).\n")

    lines.append("\n## Distribution par famille\n")
    for fam, count in family_counts.items():
        title = cand[cand["concept_family_id"] == fam].iloc[0]["concept_family_title"]
        lines.append(f"- {fam} — {title} : {count}\n")
    lines.append("\n## Distribution par système\n")
    for sys, count in system_counts.items():
        lines.append(f"- {sys} : {count}\n")

    lines.append("\n## Preuves Maia/Lichess utilisées\n")
    lines.append("- Source scorecards : DATA/scorecards_validated_expanded_corrected.csv.\n")
    lines.append("- Source synthèse corrigée : DATA/corrected_validation_summary.json.\n")
    lines.append("- Source GPU full-policy : DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess_summary.json.\n")
    if "gpu_full_policy_groups_observed" in decisions.columns:
        gpu_groups = decisions["gpu_full_policy_groups_observed"].dropna().astype(str).replace("", pd.NA).dropna()
        gpu_top3 = decisions["gpu_top3_agreement_rate"].dropna().astype(str).replace("", pd.NA).dropna()
        if not gpu_groups.empty:
            lines.append(f"- Groupes Maia GPU observés : {gpu_groups.iloc[0]} ; top3 agreement full-policy/Lichess : {gpu_top3.iloc[0] if not gpu_top3.empty else 'n/a'}.\n")
    lines.append("- La rareté ne condamne pas automatiquement un concept sain ; elle baisse la priorité core, le poids MoveTrainer et signale un besoin de bêta humaine.\n")

    lines.append("\n## Note audit moteur candidat\n")
    lines.append("Le PGN candidat doit être réaudité dans DATA/stockfish_v1_1_candidate_500k.csv, puis les commentaires BILAN V1.1 sont régénérés exclusivement depuis ce CSV.\n")
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
