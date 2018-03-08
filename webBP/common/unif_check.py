import math
import numpy as np


def get_index_from_p_value(p_value: float, interval_length: float) -> int:
    pos = int(math.floor(p_value * 10))
    if pos >= 10:
        pos -= 1
    delta = int(round(interval_length / 0.1))
    ret = int(pos / delta)
    return ret


def insert_into_2d_array(values1: list, values2: list, arr_size: int) -> np.ndarray:
    if len(values1) != len(values2):
        raise RuntimeError('Lists do not have the same size: ({}, {})'.format(len(values1), len(values2)))
    arr = np.zeros((arr_size, arr_size), dtype=np.uint64)
    interval_length = 1.0 / float(arr_size)
    for i in range(len(values1)):
        v1 = values1[i]
        v2 = values2[i]
        x = get_index_from_p_value(v1, interval_length)
        y = get_index_from_p_value(v2, interval_length)
        arr[y][x] += 1
    return arr


def check_for_uniformity(p_values1: list, p_values2: list):
    if len(p_values1) != len(p_values2):
        raise RuntimeError('Lists do not have the same size: ({}, {})', len(p_values1), len(p_values2))
    return False
