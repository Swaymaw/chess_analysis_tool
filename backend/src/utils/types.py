from enum import Enum


class EngineTypes(str, Enum):
    STOCKFISH = "stockfish"
    LC0 = "lc0"


class Side(str, Enum):
    WHITE = "white"
    BLACK = "black"


class MoveQuality(str, Enum):
    BLUNDER = "blunder"
    MISTAKE = "mistake"
    INACCURACY = "inaccuracy"
    GOOD = "good"
    EXCELLENT = "excellent"
    BEST = "best"
    BRILLIANT = "brilliant"
