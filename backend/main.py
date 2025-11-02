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
    Generates a human-readable summary of the game move by move for the given player side.

    Args:
        pgn (str): The PGN (Portable Game Notation) string representing the chess game.
        side (Side): The player's side ("white" or "black").
                        Accepts string values "white" or "black", which are internally mapped to the `Side` enum.

    Returns:
        str: A summary of the game for the specified side.
    """
    engine: SimpleEngine = get_engine(EngineTypes.STOCKFISH)

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
