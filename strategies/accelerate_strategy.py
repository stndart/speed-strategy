import numpy as np
from typing import Callable
from .common import *

# runs simulation of strategy until target.x is achieved or until coords.y hits 0
def simulate(start_speed: float, start_angle: float,
             acceleration: float, rotation: Callable[[float], float],
             target: np.ndarray[float],
             delta: float = PRECISION):
    coords = np.array([0, 0], dtype=float)
    speed_vec = rotate(np.array([1, 0]), -start_angle)
    speed = start_speed
    t: float = 0.0
    while coords[1] >= 0 and coords[0] <= target[0] and speed > 0:
        coords += speed * speed_vec * delta

        speed += acceleration * delta
        angle = rotation(speed) * delta
        speed_vec = rotate(speed_vec, angle)
        t += delta
    
    return t, coords

# achieves target either by lowering rotation or acceleration
def achieve(target: np.ndarray[float],
            start_speed: float, start_angle: float,
            max_acceleration: float, rotation: Callable[[float], float],
            delta: float = PRECISION):
    t, s = simulate(start_speed, start_angle, max_acceleration, rotation, target, delta=delta)
    
    # we achieved x = x before y = 0, => going too fast
    if s[1] >= 0:
        acc_mod = achieve_acceleration(target,
            start_speed, start_angle,
            max_acceleration, rotation,
            delta=delta)
        acceleration = acc_mod * max_acceleration
        rot = rotation
    else:
        rot_mod = achieve_rotation(target,
            start_speed, start_angle,
            max_acceleration, rotation,
            delta=delta)
        rot = make_rotation(rotation, rot_mod)
        acceleration = max_acceleration
    return simulate(start_speed, start_angle, acceleration, rot, target, delta=delta)

# achieves target by lowering acceleration
def achieve_acceleration(target: np.ndarray[float],
            start_speed: float, start_angle: float,
            max_acceleration: float, rotation: Callable[[float], float],
            delta: float = PRECISION, precision: float = BPRECISION):
    # probably won't achieve
    L = -1
    # checks if we even can achieve:
    t, s = simulate(start_speed, start_angle, 0, rotation, target, delta=delta)
    if s[1] >= 0:
        return -1
    # too fast
    R = 1
    while R - L > precision:
        m = (L + R) / 2
        t, s = simulate(start_speed, start_angle, max_acceleration * m, rotation, target, delta=delta)
        # still too fast
        if s[1] >= 0:
            R = m
        else:
            L = m
    return R

def make_rotation(rotation: Callable[[float], float], rot_mod: float):
    def func(speed: float):
        return rotation(speed) * rot_mod
    return func

def achieve_rotation(target: np.ndarray[float],
            start_speed: float, start_angle: float,
            max_acceleration: float, rotation: Callable[[float], float],
            delta: float = PRECISION, precision: float = BPRECISION):
    # certainly won't achieve
    L = 0
    # too fast rotation
    R = 1
    while R - L > precision:
        m = (L + R) / 2
        t, s = simulate(start_speed, start_angle, max_acceleration * m, rotation, target, delta=delta)
        # still too fast rotation
        if s[1] < 0:
            R = m
        else:
            L = m
    return R