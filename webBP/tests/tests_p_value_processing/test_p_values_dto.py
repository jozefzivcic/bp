from unittest import TestCase

from p_value_processing.p_values_dto import PValuesDto
from tests.tests_p_value_processing.common_data import dict_for_test_13, dict_for_test_14


class TestPValuesDto(TestCase):
    def setUp(self):
        self.dto_13 = PValuesDto(dict_for_test_13)
        self.dto_14 = PValuesDto(dict_for_test_14)

    def test_results(self):
        expected_p_values = dict_for_test_13['results']
        ret = self.dto_13.get_results_p_values()
        self.assertEqual(expected_p_values, ret)