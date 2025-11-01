from enum import Enum


class Engine(str, Enum):
    STOCKFISH = "stockfish"


class Side(str, Enum):
    WHITE = "white"
    BLACK = "black"
