import chess
from chess.engine import Cp, Limit, PovScore, SimpleEngine

from src.utils.config import MATE_SCORE
from src.utils.helper import get_engine, uci_to_san
from src.utils.types import EngineTypes


def move_scoring(
    board: chess.Board,
    move: chess.Move,
    player: chess.Color,
    engine_type: EngineTypes = EngineTypes.STOCKFISH,
    time_per_move: float = 1.0,
) -> tuple[chess.Move, float, float]:
    engine: SimpleEngine = get_engine(engine_type)

    # analyzing the current position
    info = engine.analyse(board, Limit(time=time_per_move))
    best_move = info.get("pv", [move])[0]

    bs = info.get("score", PovScore(relative=Cp(0), turn=player)).pov(player)
    best_move_score = bs.score(mate_score=MATE_SCORE)

    # # pushed the move on a copied board
    # b_best = board.copy()
    # b_best.push(best_move)
    # info_best = engine.analyse(b_best, Limit(time=time_per_move))
    # bs = info_best.get("score", PovScore(relative=Cp(0), turn=player)).pov(player)
    # best_move_score = bs.score(mate_score=100000)

    # pushed user's move on a copied board
    b_my = board.copy()
    b_my.push(move)
    info_my = engine.analyse(b_my, Limit(time=time_per_move))
    ms = info_my.get("score", PovScore(relative=Cp(0), turn=player)).pov(player)
    my_move_score = ms.score(mate_score=MATE_SCORE)

    return best_move, best_move_score, my_move_score


def best_line(
    board: chess.Board,
    engine_type: EngineTypes = EngineTypes.STOCKFISH,
    time_per_move: float = 1.0,
    max_depth: int = 10,
) -> list[str]:

    best_moves = []
    engine: SimpleEngine = get_engine(engine_type)

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
