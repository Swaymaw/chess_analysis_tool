import math
from io import StringIO

import chess
import chess.pgn

from src.modules.engine_insights import best_line, move_scoring
from src.utils.helper import chess_line_formatter, move_eval_formatter, uci_to_san


def get_engine_summary(
    pgn_str: str,
    player: chess.Color,
    include_lines: bool = True,
    line_depth: int = 5,
    time_per_move: float = 0.5,
):
    game = chess.pgn.read_game(StringIO(pgn_str))

    if game is None:
        return "Failed to read PGN file. Incorrect PGN file format."

    white_player = game.headers.get("White", "White")
    black_player = game.headers.get("Black", "Black")

    board = game.board()

    response = ""

    # response += board +"\n<------>\n"
    for i, move in enumerate(game.mainline_moves()):
        best_move, best_move_score, my_move_score = move_scoring(
            board, move, player, time_per_move=time_per_move
        )

        b_bm = board.copy()
        b_bm.push(best_move)

        response += move_eval_formatter(
            move_count=math.ceil((i + 1) / 2),
            player_name=white_player if i % 2 == 0 else black_player,
            my_move=uci_to_san(move, board),
            best_move=uci_to_san(best_move, board),
            best_move_score=best_move_score,
            my_move_score=my_move_score,
        )

        if include_lines:
            best_move_san = uci_to_san(best_move, board)
            engine_line = best_line(
                b_bm, time_per_move=time_per_move, max_depth=line_depth
            )
            response += chess_line_formatter([best_move_san] + engine_line)

        response += "\n<----->\n\n"
        board.push(move)

    return response
