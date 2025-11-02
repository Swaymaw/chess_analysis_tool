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


def fmt(s):
    if s is None:
        return "mate"
    return f"{s / 100:.2f}"


def move_eval_formatter(
    move_count: int,
    player_name: str,
    my_move: str,
    best_move: str,
    best_move_score: float,
    my_move_score: float,
):
    summary = f"""
        MoveCount: {move_count}
        PlayerName: {player_name}
        MyMove: {my_move} | BestMove: {best_move}
        MyMoveScore: {fmt(my_move_score)} | BestMoveScore: {fmt(best_move_score)}
        MyMove vs BestMove: {(best_move_score - my_move_score) / 100:.2f}
    """
    return summary
