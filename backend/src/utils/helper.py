from functools import lru_cache

import chess.engine

from src.utils.config import ENGINE_PATHS, WEIGHTS_FILE
from src.utils.types import EngineTypes


@lru_cache(maxsize=1)
def get_engine(engine_type: EngineTypes) -> chess.engine.SimpleEngine:
    if engine_type == EngineTypes.STOCKFISH:
        return chess.engine.SimpleEngine.popen_uci(ENGINE_PATHS["stockfish"])
    elif engine_type == EngineTypes.LC0:
        engine: chess.engine.SimpleEngine = chess.engine.SimpleEngine.popen_uci(
            ENGINE_PATHS["lc0"]
        )
        engine.configure({"WeightsFile": WEIGHTS_FILE.get("maia-2200")})
        return engine


def fmt(s: float):
    return f"{s / 100:.2f}"


def move_eval_formatter(
    move_count: int,
    my_move: str,
    best_move: str,
    best_move_score: float,
    my_move_score: float,
):
    summary = f"""
        MoveCount: {move_count}
        MyMove: {my_move} | BestMove: {best_move}
        MyMoveScore: {fmt(my_move_score)} | BestMoveScore: {fmt(best_move_score)}
    """
    return summary


def chess_line_formatter(moves: list[str]):
    summary = f"""
        BestLine: {" ".join(moves).strip()}
    """
    return summary


def uci_to_san(move: chess.Move, board: chess.Board) -> str:
    """
    Converts a UCI move to Standard Algebraic Notation (SAN).

    Args:
        move (chess.Move): The UCI string of the move (e.g., "e2e4", "g1f3").
        board: (chess.Board): Board Position

    Returns:
        str: The SAN representation of the move (e.g., "e4", "Nf3").
             Returns None if the UCI string is invalid for the given board.
    """

    try:
        if move in board.legal_moves:
            return board.san(move)
        else:
            return ""
    except ValueError:
        return ""
