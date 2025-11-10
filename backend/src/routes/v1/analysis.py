from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import ORJSONResponse

from src.modules.engine_insights import best_line, move_scoring
from src.schemas.app_schema import MoveAnalyze
from src.utils.helper import chess_line_formatter, move_eval_formatter

analysis_router = APIRouter(prefix="/analysis")


@analysis_router.get("/move_analyze")
def move_analysis(data: Annotated[MoveAnalyze, Query()]):

    best_move, best_move_score, my_move_score = move_scoring(
        fen=data.fen, move=data.move, side=data.orientation
    )

    move_eval = move_eval_formatter(
        move_count=data.moveIndex,
        player_name="swaymaw",
        my_move=data.move,
        best_move=best_move,
        best_move_score=best_move_score,
        my_move_score=my_move_score,
    )
    engine_line = best_line(fen=data.fen)

    line_description = chess_line_formatter(engine_line)

    return ORJSONResponse(content={"description": move_eval + line_description})
