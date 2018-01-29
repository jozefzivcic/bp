from itertools import repeat
from unittest import TestCase
from unittest.mock import MagicMock

from charts.p_values.data_for_p_values_drawer import DataForPValuesDrawer
from charts.p_values.extractor import Extractor
from charts.p_values_chart_dto import PValuesChartDto
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, TestsIdData
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test


class TestExtractor(TestCase):
    def setUp(self):
        self.p_values_chart_dto = PValuesChartDto()
        self.p_values_chart_dto.title = 'p-values from selected tests'
        self.p_values_chart_dto.x_label = 'test'
        self.p_values_chart_dto.y_label = 'p-value'

        storage_mock = MagicMock()
        storage_mock.nist = 'nist'
        self.extractor = Extractor(None, storage_mock)
        self.extractor._test_dao.get_test_by_id = MagicMock(side_effect=db_test_dao_get_test_by_id)
        self.extractor._nist_dao.get_nist_param_for_test = MagicMock(side_effect=nist_dao_get_nist_param_for_test)

        self.test1_id = TestsIdData.test1_id
        self.test1_name = 'Frequency'
        self.test2_id = TestsIdData.test2_id
        self.test2_name = 'Cumulative Sums'

        self.non_existing_test_id = TestsIdData.non_existing_test_id

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
        p_values_dto = PValuesDto(dict_for_test_13)
        data = DataForPValuesDrawer()
        self.extractor.add_data(self.p_values_chart_dto, p_values_dto, data, self.test1_id)

        expected = [self.test1_name]
        self.assertEqual(expected, data.x_ticks_labels)

        expected = [1]
        self.assertEqual(expected, data.x_ticks_positions)

        expected = list(repeat(1, 10))
        self.assertEqual(expected, data.x_values)

        expected = dict_for_test_13['results']
        self.assertEqual(expected, data.y_values)

        self.assertEqual(2, self.extractor._i)

    def test_add_data_index_one(self):
        p_values_dto = PValuesDto(dict_for_test_14)
        data = DataForPValuesDrawer()
        self.extractor.add_data(self.p_values_chart_dto, p_values_dto, data, self.test2_id, 1)

        expected = [self.test2_name + '_1']
        self.assertEqual(expected, data.x_ticks_labels)

        expected = [1]
        self.assertEqual(expected, data.x_ticks_positions)

        expected = list(repeat(1, 10))
        self.assertEqual(expected, data.x_values)

        expected = dict_for_test_14['data1']
        self.assertEqual(expected, data.y_values)

        self.assertEqual(2, self.extractor._i)

    def test_add_data_none_index_zoomed(self):
        self.p_values_chart_dto.zoomed = True
        alpha = dict_for_test_13['results'][0]
        self.p_values_chart_dto.alpha = alpha

        p_values_dto = PValuesDto(dict_for_test_13)
        data = DataForPValuesDrawer()
        self.extractor.add_data(self.p_values_chart_dto, p_values_dto, data, self.test1_id)

        expected = [self.test1_name]
        self.assertEqual(expected, data.x_ticks_labels)

        expected = [1]
        self.assertEqual(expected, data.x_ticks_positions)

        expected_p_values = [p_value for p_value in dict_for_test_13['results'] if p_value <= alpha]

        expected = list(repeat(1, len(expected_p_values)))
        self.assertEqual(expected, data.x_values)

        expected = expected_p_values
        self.assertEqual(expected, data.y_values)

        self.assertEqual(2, self.extractor._i)

    def test_add_data_index_one_zoomed(self):
        self.p_values_chart_dto.zoomed = True
        alpha = dict_for_test_14['data1'][0]
        self.p_values_chart_dto.alpha = alpha

        p_values_dto = PValuesDto(dict_for_test_14)
        data = DataForPValuesDrawer()
        self.extractor.add_data(self.p_values_chart_dto, p_values_dto, data, self.test2_id, 1)

        expected = [self.test2_name + '_1']
        self.assertEqual(expected, data.x_ticks_labels)

        expected = [1]
        self.assertEqual(expected, data.x_ticks_positions)

        expected_p_values = [p_value for p_value in dict_for_test_14['data1'] if p_value <= alpha]

        expected = list(repeat(1, len(expected_p_values)))
        self.assertEqual(expected, data.x_values)

        expected = expected_p_values
        self.assertEqual(expected, data.y_values)

        self.assertEqual(2, self.extractor._i)

    def test_get_data_from_acc(self):
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        acc = PValuesAccumulator()
        acc.add(self.test1_id, dto_13)
        acc.add(self.test2_id, dto_14)

        data = self.extractor.get_data_from_accumulator(acc, self.p_values_chart_dto)

        expected = 0.01
        self.assertAlmostEqual(expected, data.alpha, places=1E-6)

        expected = list(repeat(1, 10))
        expected.extend(list(repeat(2, 10)))
        expected.extend(list(repeat(3, 10)))
        self.assertEqual(expected, data.x_values)

        expected = list(dict_for_test_13['results'])
        expected.extend(list(dict_for_test_14['data1']))
        expected.extend(list(dict_for_test_14['data2']))
        self.assertEqual(expected, data.y_values)

        expected = [1, 2, 3]
        self.assertEqual(expected, data.x_ticks_positions)

        expected = [self.test1_name, self.test2_name + '_1', self.test2_name + '_2']
        self.assertEqual(expected, data.x_ticks_labels)

        expected = 'test'
        self.assertEqual(expected, data.x_label)

        expected = 'p-value'
        self.assertEqual(expected, data.y_label)

        expected = 'p-values from selected tests'
        self.assertEqual(expected, data.title)
