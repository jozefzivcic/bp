from unittest import TestCase
from unittest.mock import patch

import numpy as np
from scipy.stats import chisquare

from common.unif_check import UnifCheck

threshold = 1E-6


class TestUnifCheck(TestCase):
    def setUp(self):
        self.unif_check = UnifCheck(0.01, 5)

    def test_is_approx_fulfilled_raises_exception(self):
        with self.assertRaises(RuntimeError) as ex:
            self.unif_check.is_approx_fulfilled()
        self.assertEqual('Verify, compute or check must be called first', str(ex.exception))

    def test_is_approx_fulfilled(self):
        unif_check = UnifCheck(0.01, 5)
        unif_check.verify_approximation([0.1, 0.2, 0.3])
        ret = unif_check.is_approx_fulfilled()
        self.assertIsNotNone(ret)
        self.assertEqual(bool, type(ret))

        unif_check = UnifCheck(0.01, 5)
        unif_check.compute_chisq_p_value([0.1, 0.2, 0.3], [0.1, 0.2, 0.3])
        ret = unif_check.is_approx_fulfilled()
        self.assertIsNotNone(ret)
        self.assertEqual(bool, type(ret))

        unif_check = UnifCheck(0.01, 5)
        unif_check.compute_chisq_p_value([0.1, 0.2, 0.3], [0.1, 0.2, 0.3])
        ret = unif_check.is_approx_fulfilled()
        self.assertIsNotNone(ret)
        self.assertEqual(bool, type(ret))

    def test_verify_condition_true_q_one(self):
        categories = [5, 5, 6, 50, 20, 7, 12]
        ret = self.unif_check.verify_condition(categories, 1)
        self.assertTrue(ret)

    def test_verify_condition_false_q_one(self):
        categories = [5, 4, 6, 50, 20, 7, 12]
        ret = self.unif_check.verify_condition(categories, 1)
        self.assertFalse(ret)

    def test_verify_condition_true_q_decimal(self):
        categories = [8, 8, 9, 50, 20, 10, 12]
        ret = self.unif_check.verify_condition(categories, 1.5)
        self.assertTrue(ret)

    def test_verify_condition_false_q_decimal(self):
        categories = [8, 8, 9, 50, 20, 7, 10, 12]
        ret = self.unif_check.verify_condition(categories, 1.5)
        self.assertFalse(ret)

    @patch('common.unif_check.UnifCheck.verify_condition')
    def test_verify_yarnold(self, method):
        categories = [4, 5, 6, 5, 1, 10, 12]
        q = 2 / 7
        self.unif_check.verify_yarnold(categories)
        method.assert_called_once_with(categories, q)

    @patch('common.unif_check.UnifCheck.verify_yarnold')
    def test_verify_approximation_first_succeeds(self, method):
        categories = [5, 5, 6, 10, 7, 6]
        self.unif_check.verify_approximation(categories)
        self.assertTrue(self.unif_check.is_approx_fulfilled())
        self.assertEqual(0, method.called)

    def test_verify_approximation_yarnold_succeeds(self):
        categories = [5, 3, 3, 3, 7, 6]
        self.unif_check.verify_approximation(categories)
        self.assertTrue(self.unif_check.is_approx_fulfilled())

    def test_verify_approximation_yarnold_fails(self):
        categories = [5, 2, 3, 3, 7, 6]
        self.unif_check.verify_approximation(categories)
        self.assertFalse(self.unif_check.is_approx_fulfilled())

    def test_compute_chisq_p_value_raises_exception(self):
        with self.assertRaises(RuntimeError) as ex:
            self.unif_check.compute_chisq_p_value([1, 2, 3], [1, 2, 3, 4])
        self.assertEqual('Lists do not have the same size: (3, 4)', str(ex.exception))

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
