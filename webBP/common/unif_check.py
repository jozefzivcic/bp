import math
import numpy as np
from itertools import repeat
from scipy.stats import chisquare


def get_index_from_p_value(p_value: float, interval_length: float) -> int:
    pos = int(math.floor(p_value * 10))
    if pos >= 10:
        pos -= 1
    delta = int(round(interval_length / 0.1))
    ret = int(pos / delta)
    return ret


def insert_into_2d_array(values1: list, values2: list, arr_dim: int) -> np.ndarray:
    if len(values1) != len(values2):
        raise RuntimeError('Lists do not have the same size: ({}, {})'.format(len(values1), len(values2)))
    arr = np.zeros((arr_dim, arr_dim), dtype=np.uint64)
    interval_length = 1.0 / float(arr_dim)
    for i in range(len(values1)):
        v1 = values1[i]
        v2 = values2[i]
        x = get_index_from_p_value(v1, interval_length)
        y = get_index_from_p_value(v2, interval_length)
        arr[y][x] += 1
    return arr


def compute_chisq_p_value(p_values1: list, p_values2: list, size: int) -> float:
    arr = insert_into_2d_array(p_values1, p_values2, size)
    flatten_arr = arr.flatten()
    prob = 1 / (size * size)
    expected = repeat(prob, size * size)
    chisq, p_value = chisquare(f_obs=flatten_arr, f_exp=expected)
    return p_value


def check_for_uniformity(p_values1: list, p_values2: list, alpha: float) -> bool:
    """
    Checks whether p_values are uniformly distributed across area of rectangular shape with side of size 1.0.
    Null hypothesis H0: Empirical and theoretical distribution are consistent.
    :param p_values1: First list of p-values.
    :param p_values2: Second list of p-values.
    :param alpha: Confidence level for hypothesis rejection.
    :return: False if we do not reject the hypothesis i.e.: p_value > alpha, True otherwise.
    """
    if len(p_values1) != len(p_values2):
        raise RuntimeError('Lists do not have the same size: ({}, {})'.format(len(p_values1), len(p_values2)))
    size = 5
    p_value = compute_chisq_p_value(p_values1, p_values2, size)
    return p_value <= alpha
