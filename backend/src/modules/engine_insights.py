import io
from functools import lru_cache

import chess
import chess.pgn
from chess.engine import Cp, Limit, PovScore, SimpleEngine

from src.modules.move_metrics import get_accuracy, get_move_quality
from src.utils.config import MATE_SCORE
from src.utils.helper import get_engine, uci_to_san
from src.utils.types import EngineTypes, MoveQuality


@lru_cache(maxsize=256)
def move_scoring(
    fen: str,
    move: str,
    engine_type: EngineTypes = EngineTypes.STOCKFISH,
    depth_per_move: int = 8,
) -> tuple[float, str, float, float]:

    board = chess.Board(fen)
    engine: SimpleEngine = get_engine(engine_type)

    # finding the best move for the given FEN position
    info = engine.analyse(board, Limit(depth=depth_per_move))
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

    position_eval = info.get(
        "score", PovScore(relative=Cp(0), turn=chess.WHITE)
    ).white()

    position_score = position_eval.score(mate_score=MATE_SCORE) / 100

    # push best move on a copied board and evaluate score on reached position
    b_best = board.copy()
    b_best.push_san(best_move)
    info_best = engine.analyse(b_best, Limit(depth=depth_per_move))
    bs = info_best.get("score", PovScore(relative=Cp(0), turn=chess.WHITE)).white()
    best_move_score = bs.score(mate_score=MATE_SCORE)

    if best_move == move:
        my_move_score = best_move_score

    else:
        # push user's move on a copied board and evaluate score on reached position
        b_my = board.copy()
        b_my.push_san(move)
        info_my = engine.analyse(b_my, Limit(depth=depth_per_move))
        ms = info_my.get("score", PovScore(relative=Cp(0), turn=chess.WHITE)).white()
        my_move_score = ms.score(mate_score=MATE_SCORE)

    return position_score, best_move, best_move_score, my_move_score


@lru_cache(maxsize=256)
def get_score(
    fen: str,
    engine_type: EngineTypes = EngineTypes.STOCKFISH,
    depth_per_move: int = 8,
):
    engine: SimpleEngine = get_engine(engine_type)

    game_board = chess.Board(fen=fen)

    info = engine.analyse(game_board, limit=Limit(depth=depth_per_move))

    bs = info.get("score", PovScore(relative=Cp(0), turn=chess.WHITE)).white()

    best_move_score = bs.score(mate_score=MATE_SCORE)

    return best_move_score / 100


@lru_cache(maxsize=256)
def best_line(
    fen: str,
    engine_type: EngineTypes = EngineTypes.STOCKFISH,
    depth_per_move: int = 8,
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
            info = engine.analyse(board, Limit(depth=depth_per_move))
            best_move = info.get("pv", list(board.legal_moves))[0]

            best_move_san = uci_to_san(best_move, board)
            best_moves.append(best_move_san)
            board.push(best_move)
        else:
            break

    return best_moves


@lru_cache(maxsize=256)
def per_move_score(
    pgn: str,
    engine_type: EngineTypes = EngineTypes.STOCKFISH,
    depth_per_move: float = 8,
) -> tuple[list[float], list[MoveQuality], float, float]:
    parsed_pgn = io.StringIO(pgn)
    game = chess.pgn.read_game(parsed_pgn)

    if game is None:
        return ([], [], 0.0, 0.0)

    moves = list(game.mainline_moves())

    if not moves:
        return ([], [], 0.0, 0.0)

    scores = []
    move_qualities = []
    white_cp = []
    black_cp = []
    board = chess.Board()

    for move in moves:
        position_score, _, best_move_score, my_move_score = move_scoring(
            fen=board.fen(),
            engine_type=engine_type,
            move=uci_to_san(move, board=board),
            depth_per_move=depth_per_move,
        )
        diff = best_move_score - my_move_score

        if board.turn == chess.BLACK:
            diff *= -1
        diff /= 100

        if board.turn == chess.WHITE:
            white_cp.append(abs(diff))
        else:
            black_cp.append(abs(diff))

        move_quality = get_move_quality(diff)

        move_qualities.append(move_quality)
        scores.append(position_score)
        board.push(move)

    # adding position score after last move was played on board
    position_score = get_score(
        fen=board.fen(),
        engine_type=engine_type,
        depth_per_move=depth_per_move,
    )
    scores.append(position_score)

    impact = 0
    result = game.headers["Result"]

    if result == "1-0":
        impact = 0.8
    elif result == "0-1":
        impact = -0.8

    white_acc = get_accuracy(white_cp, m=0.8, k=0.4) + (impact * 2.5)
    black_acc = get_accuracy(black_cp, m=0.8, k=0.4) - (impact * 2.5)

    return scores, move_qualities, white_acc, black_acc
