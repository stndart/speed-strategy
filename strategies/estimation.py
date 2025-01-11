import numpy as np
from typing import Callable

def estimate(start_speed: float, acceleration: float,
             distance: float, strategy: Callable,
             rotation: Callable[[float], float],
             precision: float = 1e-4) -> float:
    def success(angle: float):
        return strategy(start_speed, angle, acceleration, rotation)[1][0] < distance

    if success(np.pi / 2):
        return np.pi / 2
    
    L = 0
    R = np.pi / 2
    while R - L > precision:
        m = (L + R) / 2
        if success(m):
            L = m
        else:
            R = m
    return L