import numpy as np
from typing import Callable
from .accelerate_strategy import simulate as ac_sim, achieve as ac_ac
# from .turn_strategy import simulate as ts_sim, achieve as ts_ac

def estimate(start_speed: float, start_angle: float,
             acceleration: float,
             distance: float, strategy: Callable,
             rotation: Callable[[float], float],
             delta: float = 1e-4) -> float:
    target = np.array([distance, 0], dtype=float)
    t, c, flag = strategy(target, start_speed, start_angle, acceleration, rotation, delta=delta)
    return t if flag else float('inf')

def compare(start_speed: float, acceleration: float,
            start_angle: float,
            distance: float, strategies: list[Callable],
            rotation: Callable[[float], float],
            delta: float = 1e-4) -> list[float]:
    res = [estimate(start_speed, start_angle, acceleration, distance, s, rotation, delta=delta) for s in strategies]
    return res