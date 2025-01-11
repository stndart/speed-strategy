import numpy as np
from typing import Callable
from .common import *

def signed_angle(v1, v2):
    angle = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
    return np.arctan2(np.sin(angle), np.cos(angle))  # Normalize to [-π, π]

def turn_angle(coords: np.ndarray[float], speed_vec: np.ndarray[float], target: np.ndarray[float]):
    d = target - coords
    return signed_angle(speed_vec, d)

def simulate(start_speed: float, start_angle: float,
             acceleration: float, rotation: Callable[[float], float],
             max_time: float = 10.0,
             precision: float = PRECISION):
    coords = np.array([0, 0], dtype=float)
    speed_vec = np.array([np.cos(start_angle), np.sin(start_angle)], dtype=float) * start_speed
    speed = start_speed
    t: float = 0.0
    while coords[1] >= 0 and t < max_time:
        coords += speed_vec * speed * precision
        if turn_angle(coords, speed_vec, )

        omega = rotation(speed) * precision
        speed_vec = rotate(speed_vec, omega)
        speed += acceleration * precision
        t += precision

        # print(coords, speed_vec, speed)
    return t, coords