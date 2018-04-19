from itertools import repeat
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from charts.p_values.data_for_p_values_drawer import DataForPValuesDrawer
from charts.p_values.extractor import Extractor
from charts.dto.p_values_chart_dto import PValuesChartDto
from enums.nist_test_type import NistTestType
from models.nistparam import NistParam
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, TestsIdData, short_names_dict
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test


class TestExtractor(TestCase):
    def mock_func(self, func_name, side_effect):
        patcher = patch(func_name, side_effect=side_effect)
        self.addCleanup(patcher.stop)
        patcher.start()

    def mock(self):
        self.mock_func('managers.dbtestmanager.DBTestManager.get_test_by_id', db_test_dao_get_test_by_id)
        self.mock_func('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                       nist_dao_get_nist_param_for_test)

    def setUp(self):
        self.mock()
        self.p_values_chart_dto = PValuesChartDto()
        self.p_values_chart_dto.title = 'p-values from selected tests'
        self.p_values_chart_dto.x_label = 'test'
        self.p_values_chart_dto.y_label = 'p-value'
        self.p_values_chart_dto.test_names = short_names_dict

        storage_mock = MagicMock(nist='nist')
        self.extractor = Extractor(None, storage_mock)

        self.test1_id = TestsIdData.test1_id
        self.test1_name = short_names_dict.get(NistTestType.TEST_FREQUENCY)
        self.test2_id = TestsIdData.test2_id
        self.test2_name = short_names_dict.get(NistTestType.TEST_CUSUM)

        self.non_existing_test_id = TestsIdData.non_existing_test_id

        self.y_axis_ticks = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0]
        self.y_axis_labels = ['0.0', '0.00001', '0.0001', '0.001', '0.01', '0.1', '1.0']

    @patch('managers.dbtestmanager.DBTestManager.get_test_by_id')
    def test_get_test_name_raises(self, f_get):
        mock = MagicMock(test_table='some_table')
        f_get.return_value = mock
        with self.assertRaises(RuntimeError) as ex:
            self.extractor.get_test_name(self.non_existing_test_id, 1, short_names_dict)
        self.assertEqual('Unsupported test table "some_table"', str(ex.exception))

    def test_get_test_name_results(self):
        expected = self.test1_name
        name = self.extractor.get_test_name(self.test1_id, None, short_names_dict)
        self.assertEqual(expected, name)

    def test_get_test_name_data(self):
        expected = self.test2_name + ' data 25'
        name = self.extractor.get_test_name(self.test2_id, 25, short_names_dict)
        self.assertEqual(expected, name)

    @patch('managers.nisttestmanager.NistTestManager.get_nist_param_for_test')
    def test_get_test_name_special_param(self, f_get):
        nist_param = NistParam()
        nist_param.test_number = 2
        nist_param.special_parameter = 123
        f_get.return_value = nist_param
        expected = short_names_dict.get(NistTestType.TEST_BLOCK_FREQUENCY) + ' data 54 (123)'
        ret = self.extractor.get_test_name(self.test1_id, 54, short_names_dict)
        self.assertEqual(expected, ret)

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

        expected = [self.test2_name + ' data 1']
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

        expected = [self.test2_name + ' data 1']
        self.assertEqual(expected, data.x_ticks_labels)

        expected = [1]
        self.assertEqual(expected, data.x_ticks_positions)

        expected_p_values = [p_value for p_value in dict_for_test_14['data1'] if p_value <= alpha]

        expected = list(repeat(1, len(expected_p_values)))
        self.assertEqual(expected, data.x_values)

        expected = expected_p_values
        self.assertEqual(expected, data.y_values)

        self.assertEqual(2, self.extractor._i)

    def test_get_data_from_acc_none_ds_info(self):
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        acc = PValuesAccumulator()
        acc.add(self.test1_id, dto_13)
        acc.add(self.test2_id, dto_14)

        extracted_data = self.extractor.get_data_from_accumulator(acc, self.p_values_chart_dto)
        ex_data_list = extracted_data.get_all_data()
        self.assertEqual(1, len(ex_data_list))

        self.assertIsNone(ex_data_list[0][0])

    def test_get_data_from_acc(self):
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        acc = PValuesAccumulator()
        acc.add(self.test1_id, dto_13)
        acc.add(self.test2_id, dto_14)

        extracted_data = self.extractor.get_data_from_accumulator(acc, self.p_values_chart_dto)
        ex_data_list = extracted_data.get_all_data()
        self.assertEqual(1, len(ex_data_list))
        drawer_data = ex_data_list[0][1]

        expected = 0.01
        self.assertAlmostEqual(expected, drawer_data.alpha, places=1E-6)

        expected = list(repeat(1, 10))
        expected.extend(list(repeat(2, 10)))
        expected.extend(list(repeat(3, 10)))
        self.assertEqual(expected, drawer_data.x_values)

        expected = list(dict_for_test_13['results'])
        expected.extend(list(dict_for_test_14['data1']))
        expected.extend(list(dict_for_test_14['data2']))
        self.assertEqual(expected, drawer_data.y_values)

        expected = [1, 2, 3]
        self.assertEqual(expected, drawer_data.x_ticks_positions)

        expected = [self.test1_name, self.test2_name + ' data 1', self.test2_name + ' data 2']
        self.assertEqual(expected, drawer_data.x_ticks_labels)

        expected = 'test'
        self.assertEqual(expected, drawer_data.x_label)

        expected = 'p-value'
        self.assertEqual(expected, drawer_data.y_label)

        expected = 'p-values from selected tests'
        self.assertEqual(expected, drawer_data.title)

    @patch('charts.p_values.extractor.Extractor.filter_x_labels')
    def test_get_data_from_acc_filter_x_called(self, f_filter):
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        acc = PValuesAccumulator()
        acc.add(self.test1_id, dto_13)
        acc.add(self.test2_id, dto_14)

        self.extractor.get_data_from_accumulator(acc, self.p_values_chart_dto)
        self.assertEqual(1, f_filter.call_count)

    def test_set_y_axis_small_alpha(self):
        alpha = 0.000001
        data = DataForPValuesDrawer()
        self.extractor.set_y_axis(alpha, self.y_axis_ticks, self.y_axis_labels, data)

        expected = [0.000001, 0.00001]
        self.assertEqual(expected, data.y_axis_ticks)

        expected = ['0.0', '0.00001']
        self.assertEqual(expected, data.y_axis_labels)

        alpha = 0.0000009999
        data = DataForPValuesDrawer()
        self.extractor.set_y_axis(alpha, self.y_axis_ticks, self.y_axis_labels, data)

        expected = [0.000001, 0.00001]
        self.assertEqual(expected, data.y_axis_ticks)

        expected = ['0.0', '0.00001']
        self.assertEqual(expected, data.y_axis_labels)

    def test_set_y_axis_bigger_alpha(self):
        alpha = 0.000002
        data = DataForPValuesDrawer()
        self.extractor.set_y_axis(alpha, self.y_axis_ticks, self.y_axis_labels, data)

        expected = [0.000001, 0.000002]
        self.assertEqual(expected, data.y_axis_ticks)
        expected = ['0.0', '0.000002']
        self.assertEqual(expected, data.y_axis_labels)

        alpha = 0.000009
        data = DataForPValuesDrawer()
        self.extractor.set_y_axis(alpha, self.y_axis_ticks, self.y_axis_labels, data)

        expected = [0.000001, 0.000009]
        self.assertEqual(expected, data.y_axis_ticks)
        expected = ['0.0', '0.000009']
        self.assertEqual(expected, data.y_axis_labels)

        alpha = 0.00001
        data = DataForPValuesDrawer()
        self.extractor.set_y_axis(alpha, self.y_axis_ticks, self.y_axis_labels, data)

        expected = [0.000001, 0.00001]
        self.assertEqual(expected, data.y_axis_ticks)
        expected = ['0.0', '0.00001']
        self.assertEqual(expected, data.y_axis_labels)

        alpha = 0.000011
        data = DataForPValuesDrawer()
        self.extractor.set_y_axis(alpha, self.y_axis_ticks, self.y_axis_labels, data)

        expected = [0.000001, 0.00001, 0.000011]
        self.assertEqual(expected, data.y_axis_ticks)
        expected = ['0.0', '0.00001', '0.000011']
        self.assertEqual(expected, data.y_axis_labels)

        alpha = 0.01
        data = DataForPValuesDrawer()
        self.extractor.set_y_axis(alpha, self.y_axis_ticks, self.y_axis_labels, data)

        expected = [0.000001, 0.00001, 0.0001, 0.001, 0.01]
        self.assertEqual(expected, data.y_axis_ticks)
        expected = ['0.0', '0.00001', '0.0001', '0.001', '0.01']
        self.assertEqual(expected, data.y_axis_labels)

        alpha = 0.05
        data = DataForPValuesDrawer()
        self.extractor.set_y_axis(alpha, self.y_axis_ticks, self.y_axis_labels, data)

        expected = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.05]
        self.assertEqual(expected, data.y_axis_ticks)
        expected = ['0.0', '0.00001', '0.0001', '0.001', '0.01', '0.05']
        self.assertEqual(expected, data.y_axis_labels)

    @patch('charts.p_values.extractor.filter_chart_x_ticks', return_value=('first', 'second'))
    def test_filter_x_labels(self, f_filter):
        data = DataForPValuesDrawer()
        data.x_ticks_positions = ['pos1', 'pos2']
        data.x_ticks_labels = ['label1', 'label2']
        self.extractor.filter_x_labels(data)
        f_filter.assert_called_once_with(['pos1', 'pos2'], ['label1', 'label2'])
        self.assertEqual('first', data.x_ticks_positions)
        self.assertEqual('second', data.x_ticks_labels)
