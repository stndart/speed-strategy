import numpy as np
from scipy.spatial.transform import Rotation as R

PRECISION = 1e-2
BPRECISION = 1e-4
ROT_CONST = 10.0

def rotate(x: np.ndarray[float], angle: float) -> np.ndarray[float]:
    x_ = np.concatenate([x, [0]])
    rotmat = R.from_euler('z', angle).as_matrix()
    # return rotmat.dot(x_)[:2]
    return (x_.dot(rotmat))[:2]

def car_rotation(speed: float|np.ndarray[float], const: float = ROT_CONST) -> float:
    if not isinstance(speed, float):
        speed = np.linalg.norm(speed)
    return const / speed

def spaceship_rotation(speed: float|np.ndarray[float], const: float = ROT_CONST) -> float:
    if not isinstance(speed, float):
        speed = np.linalg.norm(speed)
    return const / np.sqrt(speed)