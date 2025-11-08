import chess
from fastmcp import FastMCP

from src.modules.game_summary import get_engine_summary
from src.utils.types import Side

mcp = FastMCP("Chess Analysis Tool")


@mcp.tool()
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
    player = chess.WHITE if side == Side.WHITE else chess.BLACK

    response = get_engine_summary(
        pgn_str=pgn, player=player, time_per_move=0.2, line_depth=3
    )

    return response


if __name__ == "__main__":
    mcp.run(transport="stdio")
