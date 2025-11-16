import math
from typing import Annotated

import chess
from fastapi import APIRouter, Query
from fastapi.responses import ORJSONResponse

from src.modules.engine_insights import (
    best_line,
    get_score,
    move_scoring,
    per_move_score,
)
from src.schemas.app_schema import GetPositionScore, MoveAnalyze, PerMoveScores
from src.utils.helper import chess_line_formatter, move_eval_formatter
from src.utils.types import MoveQuality

analysis_router = APIRouter(prefix="/analysis")


@analysis_router.get("/move_analyze")
def move_analysis(data: Annotated[MoveAnalyze, Query()]):

    best_move, best_move_score, my_move_score = move_scoring(
        fen=data.fen, move=data.move, depth_per_move=17
    )

    diff = best_move_score - my_move_score

    move_quality = None

    if data.orientation == "black":
        best_move_score *= -1
        my_move_score *= -1

    board = chess.Board(fen=data.fen)

    if board.turn == chess.BLACK:
        diff *= -1
    diff /= 100
    if diff > 1.5:
        move_quality = MoveQuality.BLUNDER
    elif diff > 1.0:
        move_quality = MoveQuality.MISTAKE
    elif diff > 0.5:
        move_quality = MoveQuality.INACCURACY
    elif diff > 0.25:
        move_quality = MoveQuality.GOOD
    elif diff > 0:
        move_quality = MoveQuality.EXCELLENT
    elif diff == 0:
        move_quality = MoveQuality.BEST
    else:
        move_quality = MoveQuality.BRILLIANT

    move_eval = move_eval_formatter(
        move_count=math.ceil(((data.moveIndex + 1) / 2)),
        player_name="swaymaw",
        my_move=data.move,
        best_move=best_move,
        best_move_score=best_move_score,
        my_move_score=my_move_score,
    )

    engine_line = best_line(
        fen=data.fen, depth_per_move=8, first_move=best_move, max_depth=8
    )

    line_description = chess_line_formatter(engine_line)

    return ORJSONResponse(
        content={
            "description": move_eval + line_description,
            "move_quality": move_quality,
        }
    )


@analysis_router.get("/per_move_score")
def per_move_scores(data: Annotated[PerMoveScores, Query()]):
    scores = per_move_score(data.pgn)
    return ORJSONResponse(content={"scores": scores})


@analysis_router.get("/get_position_score")
def get_position_score(data: Annotated[GetPositionScore, Query()]):
    score = get_score(data.fen)
    return ORJSONResponse(content={"score": score})
