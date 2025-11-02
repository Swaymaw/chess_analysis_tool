from enum import Enum


class EngineTypes(str, Enum):
    STOCKFISH = "stockfish"
    LC0 = "lc0"


class Side(str, Enum):
    WHITE = "white"
    BLACK = "black"
