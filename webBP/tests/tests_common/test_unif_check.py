from itertools import repeat

import numpy as np
from unittest import TestCase

from common.unif_check import get_index_from_p_value, insert_into_2d_array


class TestUnifCheck(TestCase):
    def test_get_index_from_p_value_basic_interval_length(self):
        values = np.arange(0.0, 1.1, step=0.1).tolist()
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.1)
            self.assertEqual(i, ret)

        values = np.arange(0.01, 1.1, step=0.1).tolist()
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.1)
            self.assertEqual(i, ret)

        values = np.arange(0.09999999999, 1.1, step=0.1).tolist()
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.1)
            self.assertEqual(i, ret)

    def test_get_index_from_p_value_doubled_interval_length(self):
        values = np.arange(0.0, 1.1, step=0.1).tolist()
        expected = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.2)
            self.assertEqual(expected[i], ret)

        values = np.arange(0.01, 1.1, step=0.1).tolist()
        expected = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.2)
            self.assertEqual(expected[i], ret)

        values = np.arange(0.09999999999, 1.1, step=0.1).tolist()
        expected = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.2)
            self.assertEqual(expected[i], ret)

    def test_insert_into_2d_array_exception(self):
        with self.assertRaises(RuntimeError) as ex:
            insert_into_2d_array([1, 2, 3], [1, 2, 3, 4], 5)
        self.assertEqual('Lists do not have the same size: (3, 4)', str(ex.exception))

    def test_insert_into_2d_array_simple(self):
        values1 = [0.1, 0.3, 0.5, 0.7, 0.9]
        values2 = [0.0, 0.0, 0.0, 0.0, 0.0]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(expected, ret))

    def test_insert_into_2d_array_all(self):
        values1 = [0.1, 0.3, 0.5, 0.7, 0.9,
                   0.1, 0.3, 0.5, 0.7, 0.9,
                   0.1, 0.3, 0.5, 0.7, 0.9,
                   0.1, 0.3, 0.5, 0.7, 0.9,
                   0.1, 0.3, 0.5, 0.7, 0.9]
        values2 = [0.1, 0.1, 0.1, 0.1, 0.1,
                   0.3, 0.3, 0.3, 0.3, 0.3,
                   0.5, 0.5, 0.5, 0.5, 0.5,
                   0.7, 0.7, 0.7, 0.7, 0.7,
                   0.9, 0.9, 0.9, 0.9, 0.9]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1]])
        self.assertTrue(np.array_equal(expected, ret))

    def test_insert_into_2d_array_border_values(self):
        values1 = [0.199999, 0.399999, 0.599999, 0.799999, 0.999999]
        values2 = [0.199999, 0.199999, 0.199999, 0.199999, 0.199999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(expected, ret))

        values1 = [0.199999, 0.399999, 0.599999, 0.799999, 0.999999]
        values2 = [0.999999, 0.999999, 0.999999, 0.999999, 0.999999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1]])
        self.assertTrue(np.array_equal(expected, ret))

        values1 = [0.199999, 0.199999, 0.199999, 0.199999, 0.199999]
        values2 = [0.199999, 0.399999, 0.599999, 0.799999, 0.999999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[1, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(expected, ret))

        values1 = [0.999999, 0.999999, 0.999999, 0.999999, 0.999999]
        values2 = [0.199999, 0.399999, 0.599999, 0.799999, 0.999999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 1]])
        self.assertTrue(np.array_equal(expected, ret))

    def test_insert_into_2d_array_more_values_in_one_cell(self):
        values1 = [0.199999, 0.199999, 0.399999, 0.399999, 0.399999, 0.599999, 0.599999]
        values2 = [0.199999, 0.199999, 0.199999, 0.199999, 0.199999, 0.599999, 0.599999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[2, 3, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 2, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(expected, ret))
