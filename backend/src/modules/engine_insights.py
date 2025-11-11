from functools import lru_cache

import chess
from chess.engine import Cp, Limit, PovScore, SimpleEngine

from src.utils.config import MATE_SCORE
from src.utils.helper import get_engine, uci_to_san
from src.utils.types import EngineTypes


@lru_cache(maxsize=256)
def move_scoring(
    fen: str,
    move: str,
    engine_type: EngineTypes = EngineTypes.STOCKFISH,
    time_per_move: float = 1.0,
) -> tuple[str, float, float]:

    board = chess.Board(fen)
    engine: SimpleEngine = get_engine(engine_type)

    # finding the best move for the given FEN position
    info = engine.analyse(board, Limit(time=time_per_move))
    best_move = uci_to_san(
        info.get(
            "pv",
            [
                # FailSafe just to avoid Type Annotation warnings
                chess.Move(
                    from_square=chess.parse_square("e4"),
                    to_square=chess.parse_square("e6"),
                )
            ],
        )[0],
        board,
    )

    # push best move on a copied board and evaluate score on reached position
    b_best = board.copy()
    b_best.push_san(best_move)
    info_best = engine.analyse(b_best, Limit(time=time_per_move))
    bs = info_best.get("score", PovScore(relative=Cp(0), turn=chess.WHITE)).white()
    best_move_score = bs.score(mate_score=MATE_SCORE)

    if best_move == move:
        my_move_score = best_move_score

    else:
        # push user's move on a copied board and evaluate score on reached position
        b_my = board.copy()
        b_my.push_san(move)
        info_my = engine.analyse(b_my, Limit(time=time_per_move))
        ms = info_my.get("score", PovScore(relative=Cp(0), turn=chess.WHITE)).white()
        my_move_score = ms.score(mate_score=MATE_SCORE)

    return best_move, best_move_score, my_move_score


@lru_cache(maxsize=256)
def best_line(
    fen: str,
    engine_type: EngineTypes = EngineTypes.STOCKFISH,
    time_per_move: float = 1.0,
    first_move: str | None = None,
    max_depth: int = 10,
) -> list[str]:

    board = chess.Board(fen)
    best_moves = []
    engine: SimpleEngine = get_engine(engine_type)

    if first_move:
        board.push_san(first_move)
        best_moves.append(first_move)

    for _ in range(max_depth):
        if not board.is_game_over():
            info = engine.analyse(board, Limit(time=time_per_move))
            best_move = info.get("pv", list(board.legal_moves))[0]

            best_move_san = uci_to_san(best_move, board)
            best_moves.append(best_move_san)
            board.push(best_move)
        else:
            break

    return best_moves
