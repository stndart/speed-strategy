import numpy as np
from typing import Callable
from .common import *

def simulate(start_speed: float, start_angle: float,
             acceleration: float, rotation: Callable[[float], float],
             precision: float = PRECISION):
    coords = np.array([0, 0])
    # speed = np.array([np.cos(start_angle), np.sin(start_angle)]) * start_speed
    t: float = 0.0
    # while coords[1] >= 0:
    #     coords += speed * precision
    #     omega = rotation(speed) * precision
    #     speed = rotate(speed, omega)
    #     speed += acceleration * precision
    return t, coords