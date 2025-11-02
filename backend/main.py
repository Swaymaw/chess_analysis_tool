import math
from io import StringIO

import chess
import chess.pgn
from chess.engine import Limit, SimpleEngine
from fastmcp import FastMCP

from src.utils.helper import get_engine, move_eval_formatter
from src.utils.types import EngineTypes, Side

mcp = FastMCP("Chess Analysis Tool")


@mcp.tool
def game_summary(pgn: str, side: Side) -> str:
    """
    Returns a summary of the game move by move for each player.

    Args:
        pgn (str): The PGN string of the game.
        side (Side): The side of the player for whom the summary is to be generated.

    Returns:
        dict: A string containing a summary for the current game.
    """
    engine: SimpleEngine = get_engine(EngineTypes.LC0)

    game = chess.pgn.read_game(StringIO(pgn))

    if game is None:
        return "Failed to read PGN file. Incorrect PGN file format."

    white_player = game.headers.get("White", "White")
    black_player = game.headers.get("Black", "Black")

    player = chess.WHITE if side == Side.WHITE else chess.BLACK

    board = game.board()

    response = ""

    # response += board +"\n<------>\n"
    for i, move in enumerate(game.mainline_moves()):
        # analyzing the current position
        info = engine.analyse(board, Limit(time=0.5))
        best_move = info.get("pv", [move])[0]

        # pushed the move on a copied board
        b_best = board.copy()
        b_best.push(best_move)
        info_best = engine.analyse(b_best, Limit(time=0.5))
        bs = info_best.get("score").pov(player)
        best_move_score = bs.score(mate_score=100000)

        # pushed user's move on a copied board
        b_my = board.copy()
        b_my.push(move)
        info_my = engine.analyse(b_my, Limit(time=0.5))
        ms = info_my.get("score").pov(player)
        my_move_score = ms.score(mate_score=100000)

        response += move_eval_formatter(
            move_count=math.ceil((i + 1) / 2),
            player_name=white_player if i % 2 == 0 else black_player,
            my_move=str(move),
            best_move=str(best_move),
            best_move_score=best_move_score,
            my_move_score=my_move_score,
        )
        response += "\n<----->\n\n"
        board.push(move)
    engine.quit()

    return response


if __name__ == "__main__":
    mcp.run(transport="stdio")
