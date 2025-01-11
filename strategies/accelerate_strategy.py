import numpy as np
from typing import Callable
from .common import *

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
    t, s = simulate(target, start_speed, start_angle, max_acceleration, rotation, delta=delta)
    
    # we achieved x = x before y = 0, => going too fast
    old_s = s
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
    t, s = simulate(target, start_speed, start_angle, acceleration, rot, delta=delta)
    if old_s[1] >= 0:
        flag = s[1] < 0
    else:
        flag = s[1] >= 0
    return t, s, flag

# achieves target by lowering acceleration
def achieve_acceleration(target: np.ndarray[float],
            start_speed: float, start_angle: float,
            max_acceleration: float, rotation: Callable[[float], float],
            delta: float = PRECISION, precision: float = BPRECISION):
    # probably won't achieve
    L = -1
    # too fast
    R = 1
    while R - L > precision:
        m = (L + R) / 2
        t, s = simulate(target, start_speed, start_angle, max_acceleration * m, rotation, delta=delta)
        # still too fast
        if s[1] >= 0:
            R = m
        else:
            L = m
    return L

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
        t, s = simulate(target, start_speed, start_angle, max_acceleration, make_rotation(rotation, m), delta=delta)
        # still too fast rotation
        # print(m, s[1])
        if s[1] < 0:
            R = m
        else:
            L = m
    return L