from itertools import repeat
from scipy.stats import chisquare

from common.helper_functions import insert_into_2d_array


class UnifCheck:
    def __init__(self, alpha, size):
        self.alpha = alpha
        self.size = size

    def compute_chisq_p_value(self, p_values1: list, p_values2: list) -> float:
        arr = insert_into_2d_array(p_values1, p_values2, self.size)
        flatten_arr = arr.flatten()
        prob = 1 / (self.size * self.size)
        expected = repeat(prob, self.size * self.size)
        chisq, p_value = chisquare(f_obs=flatten_arr, f_exp=expected)
        return p_value

    def check_for_uniformity(self, p_values1: list, p_values2: list) -> bool:
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
        p_value = self.compute_chisq_p_value(p_values1, p_values2)
        return p_value <= self.alpha
