from itertools import repeat
from scipy.stats import chisquare

from common.unif_check_helpers import insert_into_2d_array


class UnifCheck:
    def __init__(self, alpha, size):
        self._alpha = alpha
        self._size = size
        self._approx_condition = None
        self._p_value = None

    def is_approx_fulfilled(self) -> bool:
        if self._approx_condition is None:
            raise RuntimeError('Verify, compute or check must be called first')
        return self._approx_condition

    def get_p_value(self):
        if self._p_value is None:
            raise RuntimeError('p-value must be computed at first')
        return self._p_value

    def verify_condition(self, exp_frequencies: list, q: float) -> bool:
        num = 5 * q
        for item in exp_frequencies:
            if item < num:
                return False
        return True

    def verify_yarnold(self, exp_frequencies: list) -> bool:
        k = len(exp_frequencies)
        q = sum(1 for i in exp_frequencies if i < 5) / k
        return self.verify_condition(exp_frequencies, q)

    def verify_approximation(self, exp_frequencies: list):
        ret = self.verify_condition(exp_frequencies, 1)
        if ret:
            self._approx_condition = True
            return
        self._approx_condition = self.verify_yarnold(exp_frequencies)

    def compute_chisq_p_value(self, p_values1: list, p_values2: list) -> float:
        if len(p_values1) != len(p_values2):
            raise RuntimeError('Lists do not have the same size: ({}, {})'.format(len(p_values1), len(p_values2)))
        arr = insert_into_2d_array(p_values1, p_values2, self._size)
        flatten_arr = list(arr.flatten().tolist())
        n = sum(flatten_arr)
        expected_multiplicity = (1 / (self._size * self._size)) * n
        expected = list(repeat(expected_multiplicity, self._size * self._size))
        self.verify_approximation(expected)
        chisq, p_value = chisquare(f_obs=flatten_arr, f_exp=expected)
        self._p_value = p_value.item()  # return built-in float instead of float64
        return self._p_value

    def check_for_uniformity(self, p_values1: list, p_values2: list) -> bool:
        """
        Checks whether p_values are uniformly distributed across area of rectangular shape with side of size 1.0.
        Null hypothesis H0: Empirical and theoretical distribution are consistent.
        :param p_values1: First list of p-values.
        :param p_values2: Second list of p-values.
        :param alpha: Confidence level for hypothesis rejection.
        :return: True if we reject H0 i.e.: p_value < alpha, False otherwise.
        """
        if len(p_values1) != len(p_values2):
            raise RuntimeError('Lists do not have the same size: ({}, {})'.format(len(p_values1), len(p_values2)))
        p_value = self.compute_chisq_p_value(p_values1, p_values2)
        return p_value < self._alpha
