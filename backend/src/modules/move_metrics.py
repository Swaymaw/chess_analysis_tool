import math

from src.utils.types import MoveQuality


def get_move_quality(diff: float) -> MoveQuality:
    move_quality = None
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
    elif diff > -0.25:
        move_quality = MoveQuality.BEST
    else:
        move_quality = MoveQuality.BRILLIANT

    return move_quality


def get_accuracy(cp_losses: list[float], m: float = 40, k: float = 10) -> float:
    aggregated_loss = 0.0
    count = 0.0
    print("CP LOSSES:", cp_losses)
    for loss in cp_losses:
        count += 1
        aggregated_loss += 0.5 * (1 - math.tanh((loss - m) / k))

    scaled = (aggregated_loss / count) * 100

    clamped = max(0, min(scaled, 100))

    return clamped
