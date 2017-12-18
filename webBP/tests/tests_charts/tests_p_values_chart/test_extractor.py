from itertools import repeat
from unittest import TestCase
from unittest.mock import MagicMock

from charts.chart_options import ChartOptions
from charts.p_values.data_for_chart import DataForChart
from charts.p_values.extractor import Extractor
from models.nistparam import NistParam
from models.test import Test
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import dict_for_test_13


class TestExtractor(TestCase):

    def dbtest_dao_side_effect(self, test_id: int):
        test = Test()
        if test_id == self.test1_id or test_id == self.test2_id:
            test.id = test_id
            test.test_table = 'nist'
        else:
            test.id = self.non_existing_test_id
            test.test_table = 'something'
        return test

    def nist_dao_side_effect(self, test: Test):
        nist_param = NistParam()
        nist_param.test_id = test.id
        if test.id == self.test1_id:
            nist_param.test_number = 1
        elif test.id == self.test2_id:
            nist_param.test_number = 3
        else:
            nist_param.test_number = 15
        return nist_param

    def setUp(self):
        chart_options = ChartOptions()
        chart_options.title = 'p-values from selected tests'
        chart_options.x_label = 'test'
        chart_options.y_label = 'p-value'

        storage_mock = MagicMock()
        storage_mock.nist = 'nist'
        self.extractor = Extractor(chart_options, None, storage_mock)
        self.extractor._test_dao.get_test_by_id = MagicMock(side_effect=self.dbtest_dao_side_effect)
        self.extractor._nist_dao.get_nist_param_for_test = MagicMock(side_effect=self.nist_dao_side_effect)

        self.test1_id = 13
        self.test1_name = 'Frequency'
        self.test2_id = 14
        self.test2_name = 'Cumulative Sums'

        self.non_existing_test_id = 15

    def test_get_test_name(self):
        expected = self.test1_name
        name = self.extractor.get_test_name(self.test1_id)
        self.assertEqual(expected, name)

        expected = self.test2_name
        name = self.extractor.get_test_name(self.test2_id)
        self.assertEqual(expected, name)

        expected = 'Undefined'
        name = self.extractor.get_test_name(self.non_existing_test_id)
        self.assertEqual(expected, name)

    def test_replace_p_values(self):
        input = [0.857153, 0.0000009, 0.000000, 0.000001, 0.0000009999999999, 0.888660, 0.471525, 0.920344, 0.357573, 0.509254]
        expected = [0.857153, 0.000001, 0.000001, 0.000001, 0.000001, 0.888660, 0.471525, 0.920344, 0.357573, 0.509254]
        ret = self.extractor.replace_zero_p_values(input)
        self.assertEqual(expected, ret)

    def test_add_data_none_index(self):
        dto = PValuesDto(dict_for_test_13)
        data = DataForChart()
        self.extractor.add_data(dto, data, self.test1_id)

        expected = [self.test1_name]
        self.assertEqual(expected, data.x_ticks_labels)

        expected = [1]
        self.assertEqual(expected, data.x_ticks_positions)

        expected = list(repeat(1, 10))
        self.assertEqual(expected, data.x_values)

        expected = dict_for_test_13['results']
        self.assertEqual(expected, data.y_values)

        self.assertEqual(2, self.extractor._i)
