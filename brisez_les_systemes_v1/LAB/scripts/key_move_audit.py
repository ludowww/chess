from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import chess
import chess.engine
import pandas as pd

from common import fen4, score_cp


def fen6(fen: str) -> str:
    fields = fen.split()
    if len(fields) == 4:
        return fen + " 0 1"
    if len(fields) == 6:
        return fen
    raise ValueError(f"Invalid FEN: {fen!r}")


def gate(loss: int) -> str:
    if loss <= 25:
        return "PASS"
    if loss <= 50:
        return "REVIEW"
    return "REJECT"


def pv_san(board: chess.Board, pv: list[chess.Move]) -> str:
    b = board.copy(stack=False)
    out: list[str] = []
    for move in pv:
        if move not in b.legal_moves:
            break
        out.append(b.san(move))
        b.push(move)
    return " ".join(out)


def move_san(board: chess.Board, move: chess.Move) -> str:
    return board.san(move) if move in board.legal_moves else "ILLEGAL"


def analyse_record(engine: chess.engine.SimpleEngine, rec: dict, *, nodes: int, multipv: int) -> dict:
    board = chess.Board(fen6(str(rec["fen_before_key_move"])))
    move = chess.Move.from_uci(str(rec["key_move_uci"]))
    if move not in board.legal_moves:
        return {
            "line_id": rec["line_id"],
            "bias_code": rec.get("bias_code", ""),
            "title": rec.get("title", ""),
            "key_move_uci": move.uci(),
            "key_move_san": "ILLEGAL",
            "key_move_loss_cp": 100000,
            "key_move_rank_multipv": "",
            "key_move_gate": "REJECT",
            "best_move_uci": "",
            "best_move_san": "",
            "best_eval_mover_cp": "",
            "candidate_eval_mover_cp": "",
            "principal_variation_uci": "",
            "principal_variation_san": "",
            "nodes": nodes,
            "engine_id": "Stockfish 18",
        }

    infos = engine.analyse(board, chess.engine.Limit(nodes=nodes), multipv=multipv)
    if isinstance(infos, dict):
        infos = [infos]
    infos = sorted(infos, key=lambda x: x.get("multipv", 1))
    best = infos[0]
    best_move = best.get("pv", [None])[0]
    best_eval = score_cp(best, board.turn)
    rank = ""
    candidate_eval = None
    candidate_pv: list[chess.Move] = []
    for info in infos:
        pv = info.get("pv", [])
        if pv and pv[0] == move:
            rank = str(info.get("multipv", ""))
            candidate_eval = score_cp(info, board.turn)
            candidate_pv = pv
            break
    if candidate_eval is None:
        cinfo = engine.analyse(board, chess.engine.Limit(nodes=nodes), root_moves=[move])
        candidate_eval = score_cp(cinfo, board.turn)
        candidate_pv = cinfo.get("pv", [move])
    loss = max(0, best_eval - candidate_eval)
    return {
        "line_id": rec["line_id"],
        "bias_code": rec.get("bias_code", ""),
        "title": rec.get("title", ""),
        "key_move_uci": move.uci(),
        "key_move_san": move_san(board, move),
        "key_move_loss_cp": int(loss),
        "key_move_rank_multipv": rank,
        "key_move_gate": gate(int(loss)),
        "best_move_uci": best_move.uci() if best_move else "",
        "best_move_san": move_san(board, best_move) if best_move else "",
        "best_eval_mover_cp": int(best_eval),
        "candidate_eval_mover_cp": int(candidate_eval),
        "principal_variation_uci": " ".join(m.uci() for m in candidate_pv),
        "principal_variation_san": pv_san(board, candidate_pv),
        "nodes": nodes,
        "engine_id": "Stockfish 18",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit objective quality of manifest key moves with Stockfish.")
    parser.add_argument("--manifest", default="DATA/core_40_index.csv")
    parser.add_argument("--engine", default="/usr/local/bin/stockfish18")
    parser.add_argument("--nodes", type=int, default=500000)
    parser.add_argument("--multipv", type=int, default=8)
    parser.add_argument("--threads", type=int, default=2)
    parser.add_argument("--hash-mb", type=int, default=512)
    parser.add_argument("--output", default="DATA/key_move_audit_v1_1.csv")
    args = parser.parse_args(argv)

    if args.nodes < 500000:
        raise SystemExit("--nodes must be at least 500000")
    if args.multipv < 8:
        raise SystemExit("--multipv must be at least 8")
    manifest = pd.read_csv(args.manifest)
    rows: list[dict] = []
    with chess.engine.SimpleEngine.popen_uci(args.engine) as engine:
        engine.configure({"Threads": args.threads, "Hash": args.hash_mb})
        for rec in manifest.to_dict("records"):
            rows.append(analyse_record(engine, rec, nodes=args.nodes, multipv=args.multipv))
    cols = [
        "line_id", "bias_code", "title", "key_move_uci", "key_move_san", "key_move_loss_cp",
        "key_move_rank_multipv", "key_move_gate", "best_move_uci", "best_move_san",
        "best_eval_mover_cp", "candidate_eval_mover_cp", "principal_variation_uci",
        "principal_variation_san", "nodes", "engine_id",
    ]
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {out} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
