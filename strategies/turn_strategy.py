import numpy as np
from typing import Callable
from .common import *

def signed_angle(v1, v2):
    angle = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
    return np.arctan2(np.sin(angle), np.cos(angle))  # Normalize to [-π, π]

def turn_angle(coords: np.ndarray[float], speed_vec: np.ndarray[float], target: np.ndarray[float]):
    d = target - coords
    return signed_angle(speed_vec, d)

# runs simulation of strategy until target.x is achieved or until coords.y hits 0
def simulate(target: np.ndarray[float],
             start_speed: float, start_angle: float,
             acceleration: float, rotation: Callable[[float], float],
             delta: float = PRECISION):
    coords = np.array([0, 0], dtype=float)
    speed_vec = rotate(np.array([1, 0]), -start_angle)
    speed = start_speed
    t: float = 0.0
    while coords[1] >= 0 and coords[0] <= target[0] and speed > 0:
        coords += speed * speed_vec * delta

        max_angle = turn_angle(coords, speed_vec, target)
        angle = rotation(speed) * delta
        if abs(angle) > abs(max_angle):
            angle = max_angle
            speed += acceleration * delta
        speed_vec = rotate(speed_vec, angle)
        t += delta
    
    return t, coords

def achieve(target: np.ndarray[float],
            start_speed: float, start_angle: float,
            max_acceleration: float, rotation: Callable[[float], float],
            delta: float = PRECISION):
    return simulate(target, start_speed, start_angle, max_acceleration, rotation, delta=delta)