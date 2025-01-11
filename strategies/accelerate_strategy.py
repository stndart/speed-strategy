import numpy as np
from typing import Callable
from .common import *

def simulate(start_speed: float, start_angle: float,
             acceleration: float, rotation: Callable[[float], float],
             precision: float = PRECISION):
    coords = np.array([0, 0], dtype=float)
    speed_vec = np.array([np.cos(start_angle), np.sin(start_angle)], dtype=float) * start_speed
    speed = start_speed
    t: float = 0.0
    while coords[1] >= 0:
        coords += speed_vec * speed * precision
        omega = rotation(speed) * precision
        speed_vec = rotate(speed_vec, omega)
        speed += acceleration * precision
        t += precision

        # print(coords, speed_vec, speed)
    return t, coords