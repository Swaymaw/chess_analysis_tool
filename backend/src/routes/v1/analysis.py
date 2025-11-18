import math
from typing import Annotated

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

analysis_router = APIRouter(prefix="/analysis")


@analysis_router.get("/move_analyze")
def move_analysis(data: Annotated[MoveAnalyze, Query()]):

    _, best_move, best_move_score, my_move_score = move_scoring(
        fen=data.fen, move=data.move, depth_per_move=17
    )

    if data.orientation == "black":
        best_move_score *= -1
        my_move_score *= -1

    move_eval = move_eval_formatter(
        move_count=math.ceil(((data.moveIndex + 1) / 2)),
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
        }
    )


@analysis_router.get("/per_move_score")
def per_move_scores(data: Annotated[PerMoveScores, Query()]):
    scores, move_qualities, white_acc, black_acc = per_move_score(
        data.pgn, depth_per_move=17
    )

    return ORJSONResponse(
        content={
            "scores": scores,
            "move_qualities": move_qualities,
            "white_acc": white_acc,
            "black_acc": black_acc,
        }
    )


@analysis_router.get("/get_position_score")
def get_position_score(data: Annotated[GetPositionScore, Query()]):
    score = get_score(data.fen)
    return ORJSONResponse(content={"score": score})
