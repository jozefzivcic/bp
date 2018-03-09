from unittest import TestCase

import numpy as np
from scipy.stats import chisquare

from common.unif_check import UnifCheck

threshold = 1E-6


class TestUnifCheck(TestCase):
    def setUp(self):
        self.unif_check = UnifCheck(0.01, 5)

    def test_check_for_uniformity_raises_exception(self):
        with self.assertRaises(RuntimeError) as ex:
            self.unif_check.check_for_uniformity([1, 2, 3], [1, 2, 3, 4])
        self.assertEqual('Lists do not have the same size: (3, 4)', str(ex.exception))

    def test_scipy_stats_chisq_uniform_data(self):
        empirical = [32309, 30126, 35010, 34761, 34955, 32883, 33255, 31604, 31173, 30536, 28571, 29467]
        n = sum(empirical)
        pj = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], dtype=float) / 365.0
        theoretical = pj * n
        theoretical = theoretical.tolist()
        chisq, p_value = chisquare(f_obs=empirical, f_exp=theoretical)
        chisq_float = chisq.item()
        p_value_float = p_value.item()
        self.assertLessEqual(abs(chisq_float - 1506.152574), threshold)
        self.assertLessEqual(0.0, p_value_float)

    def test_scipy_stats_chisq_binom_data(self):
        empirical = [3, 10, 22, 31, 14, 4]
        n = sum(empirical)
        pj = np.array([0.03125, 0.15625, 0.31250, 0.31250, 0.15625, 0.03125])
        theoretical = pj * n
        theoretical = theoretical.tolist()
        chisq, p_value = chisquare(f_obs=empirical, f_exp=theoretical)
        chisq_float = chisq.item()
        p_value_float = p_value.item()
        self.assertLessEqual(abs(chisq_float - 3.1238095), threshold)
        self.assertLessEqual(abs(p_value_float - 0.6809048), threshold)
