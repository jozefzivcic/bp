from unittest import TestCase

from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14
from p_value_processing.p_values_dto import PValuesDto


class TestPValuesDtoOnTest13(TestCase):
    def setUp(self):
        self.dto = PValuesDto(dict_for_test_13)

    def test_results(self):
        expected_p_values = dict_for_test_13['results']
        ret = self.dto.get_results_p_values()
        self.assertEqual(expected_p_values, ret)

    def test_data_raise_exception(self):
        data_num = 1
        with self.assertRaises(ValueError) as context:
            self.dto.get_data_p_values(data_num)
            self.assertTrue(str(data_num) in str(context.exception))


class TestPValuesDtoOnTest14(TestCase):
    def setUp(self):
        self.dto = PValuesDto(dict_for_test_14)

    def test_results(self):
        expected_p_values = dict_for_test_14['results']
        ret = self.dto.get_results_p_values()
        self.assertEqual(expected_p_values, ret)

    def test_data_1(self):
        expected_p_values = dict_for_test_14['data1']
        ret = self.dto.get_data_p_values(1)
        self.assertEqual(expected_p_values, ret)

    def test_data_2(self):
        expected_p_values = dict_for_test_14['data2']
        ret = self.dto.get_data_p_values(2)
        self.assertEqual(expected_p_values, ret)

    def test_data_3(self):
        data_num = 3
        with self.assertRaises(ValueError) as context:
            self.dto.get_data_p_values(data_num)
            self.assertTrue(str(data_num) in str(context.exception))

    def test_data_0(self):
        data_num = 0
        with self.assertRaises(ValueError) as context:
            self.dto.get_data_p_values(data_num)
            self.assertTrue(str(data_num) in str(context.exception))

    def test_data_not_number(self):
        data_num = 'string'
        with self.assertRaises(ValueError) as context:
            self.dto.get_data_p_values(data_num)
            self.assertTrue(str(data_num) in str(context.exception))
