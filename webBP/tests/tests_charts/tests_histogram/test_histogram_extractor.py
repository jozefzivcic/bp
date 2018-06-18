import json
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from charts.data_source_info import DataSourceInfo
from charts.extracted_data import ExtractedData
from charts.histogram.data_for_histogram_drawer import DataForHistogramDrawer
from charts.histogram.historam_extractor import HistogramExtractor
from charts.dto.histogram_dto import HistogramDto
from charts.tests_in_chart import TestsInChart
from common.error.err import Err
from common.info.info import Info
from enums.hist_for_tests import HistForTests
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, TestsIdData

intervals = ['[0.0, 0.1)', '[0.1, 0.2)', '[0.2, 0.3)', '[0.3, 0.4)', '[0.4, 0.5)', '[0.5, 0.6)', '[0.6, 0.7)',
             '[0.7, 0.8)', '[0.8, 0.9)', '[0.9, 1.0]']


def mock_add_data(ex_data: ExtractedData, global_quantities: list, all_seqcs: list, p_values: list,
                  dto: HistogramDto, test_id: int, data_num: int = None):
    if data_num is None:
        seq = PValueSequence(test_id, PValuesFileType.RESULTS)
    else:
        seq = PValueSequence(test_id, PValuesFileType.DATA, data_num)
    if HistForTests.ALL_TESTS in dto.hist_for_tests:
        all_seqcs.append(seq)


class TestHistogramExtractor(TestCase):
    def setUp(self):
        self.extractor = HistogramExtractor()
        self.quantities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sample_p_values = [0.779952, 0.468925, 0.468925, 0.511232, 0.462545, 0.666913, 0.171598, 0.375557,
                                0.746548, 0.558648]
        self.expected_quantities = [0, 1, 0, 1, 3, 2, 1, 2, 0, 0]

    @patch('json.dumps', return_value='dumps_ret')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.add_intervals_to_quantities',
           return_value='add_intervals_ret')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.add_data', side_effect=mock_add_data)
    def test_get_data_from_accumulator(self, f_add_data, f_add_intervals, f_dumps):
        dto1 = PValuesDto(dict_for_test_13)
        dto2 = PValuesDto(dict_for_test_14)
        acc = PValuesAccumulator()
        acc.add(TestsIdData.test1_id, dto1)
        acc.add(TestsIdData.test2_id, dto2)
        dto = MagicMock(x_label='x_label_str', y_label='y_label_str', title='title_str',
                        hist_for_tests=[HistForTests.ALL_TESTS, HistForTests.INDIVIDUAL_TESTS])
        ret = self.extractor.get_data_from_accumulator(acc, dto)
        ex_data_list = ret.get_all_data()
        self.assertEqual(1, len(ex_data_list))

        ds_info, data_drawer, info, err = ex_data_list[0]  # type: (DataSourceInfo, DataForHistogramDrawer, Info, Err)
        seqcs = [PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS),
                 PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1),
                 PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)]

        self.assertEqual(TestsInChart.MULTIPLE_TESTS, ds_info.tests_in_chart)
        self.assertEqual(seqcs, ds_info.p_value_sequence)
        self.assertEqual('dumps_ret', data_drawer.json_data_string)
        self.assertEqual('x_label_str', data_drawer.x_label)
        self.assertEqual('y_label_str', data_drawer.y_label)
        self.assertEqual('title_str', data_drawer.title)

        self.assertEqual(3, f_add_data.call_count)
        f_add_intervals.assert_called_once_with([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        f_dumps.assert_called_once_with('add_intervals_ret')

    @patch('json.dumps', return_value='dumps_ret')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.add_intervals_to_quantities',
           return_value='add_i_ret')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.sum_quantities')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.add_p_values_to_interval')
    def test_add_data_complete_results(self, f_add_p_values, f_sum, f_add_intervals, f_dumps):
        ex_data = ExtractedData()
        global_quantities = [1, 2, 3, 0, 0, 0, 0, 0, 0, 0]
        p_values = [1, 2, 3]
        all_seqcs = []
        dto = MagicMock(x_label='x_label_str', y_label='y_label_str', title='title_str',
                        hist_for_tests=[HistForTests.ALL_TESTS, HistForTests.INDIVIDUAL_TESTS])
        test_id = 456

        self.extractor.add_data(ex_data, global_quantities, all_seqcs, p_values, dto, test_id)

        f_add_p_values.assert_called_once_with([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], p_values)
        f_sum.assert_called_once_with([1, 2, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        f_add_intervals.assert_called_once_with([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        f_dumps.assert_called_once_with('add_i_ret')
        ex_data_list = ex_data.get_all_data()

        self.assertEqual(1, len(ex_data_list))
        ds_info, data_drawer, info, err = ex_data_list[0]  # type: (DataSourceInfo, DataForHistogramDrawer, Info, Err)
        self.assertEqual(TestsInChart.SINGLE_TEST, ds_info.tests_in_chart)
        seq = PValueSequence(test_id, PValuesFileType.RESULTS)
        self.assertEqual(seq, ds_info.p_value_sequence)
        self.assertEqual([seq], all_seqcs)
        self.assertEqual('dumps_ret', data_drawer.json_data_string)
        self.assertEqual('x_label_str', data_drawer.x_label)
        self.assertEqual('y_label_str', data_drawer.y_label)
        self.assertEqual('title_str', data_drawer.title)

    @patch('json.dumps', return_value='dumps_ret')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.add_intervals_to_quantities',
           return_value='add_i_ret')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.sum_quantities')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.add_p_values_to_interval')
    def test_add_data_complete_data(self, f_add_p_values, f_sum, f_add_intervals, f_dumps):
        ex_data = ExtractedData()
        global_quantities = [1, 2, 3, 0, 0, 0, 0, 0, 0, 0]
        p_values = [1, 2, 3]
        all_seqcs = []
        dto = MagicMock(x_label='x_label_str', y_label='y_label_str', title='title_str',
                        hist_for_tests=[HistForTests.ALL_TESTS, HistForTests.INDIVIDUAL_TESTS])
        test_id = 456
        data_num = 15
        self.extractor.add_data(ex_data, global_quantities, all_seqcs, p_values, dto, test_id, data_num)

        f_add_p_values.assert_called_once_with([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], p_values)
        f_sum.assert_called_once_with([1, 2, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        f_add_intervals.assert_called_once_with([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        f_dumps.assert_called_once_with('add_i_ret')
        ex_data_list = ex_data.get_all_data()

        self.assertEqual(1, len(ex_data_list))
        ds_info, data_drawer, info, err = ex_data_list[0]  # type: (DataSourceInfo, DataForHistogramDrawer, Info, Err)
        self.assertEqual(TestsInChart.SINGLE_TEST, ds_info.tests_in_chart)

        seq = PValueSequence(test_id, PValuesFileType.DATA, data_num)
        self.assertEqual(seq, ds_info.p_value_sequence)
        self.assertEqual([seq], all_seqcs)
        self.assertEqual('dumps_ret', data_drawer.json_data_string)
        self.assertEqual('x_label_str', data_drawer.x_label)
        self.assertEqual('y_label_str', data_drawer.y_label)
        self.assertEqual('title_str', data_drawer.title)

    @patch('charts.histogram.historam_extractor.HistogramExtractor.sum_quantities')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.add_p_values_to_interval')
    def test_add_data_only_all_tests(self, f_add_p_values, f_sum):
        ex_data = ExtractedData()
        global_quantities = [1, 2, 3, 0, 0, 0, 0, 0, 0, 0]
        p_values = [1, 2, 3]
        all_seqcs = []
        dto = MagicMock(x_label='x_label_str', y_label='y_label_str', title='title_str',
                        hist_for_tests=[HistForTests.ALL_TESTS])
        test_id = 456

        self.extractor.add_data(ex_data, global_quantities, all_seqcs, p_values, dto, test_id)

        f_add_p_values.assert_called_once_with([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], p_values)
        f_sum.assert_called_once_with([1, 2, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        ex_data_list = ex_data.get_all_data()

        self.assertEqual(0, len(ex_data_list))
        seq = PValueSequence(test_id, PValuesFileType.RESULTS)
        self.assertEqual([seq], all_seqcs)

    @patch('json.dumps', return_value='dumps_ret')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.add_intervals_to_quantities',
           return_value='add_i_ret')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.sum_quantities')
    @patch('charts.histogram.historam_extractor.HistogramExtractor.add_p_values_to_interval')
    def test_add_data_only_individual(self, f_add_p_values, f_sum, f_add_intervals, f_dumps):
        ex_data = ExtractedData()
        global_quantities = [1, 2, 3, 0, 0, 0, 0, 0, 0, 0]
        p_values = [1, 2, 3]
        all_seqcs = []
        dto = MagicMock(x_label='x_label_str', y_label='y_label_str', title='title_str',
                        hist_for_tests=[HistForTests.INDIVIDUAL_TESTS])
        test_id = 456
        data_num = 15

        self.extractor.add_data(ex_data, global_quantities, all_seqcs, p_values, dto, test_id, data_num)

        f_add_p_values.assert_called_once_with([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], p_values)
        self.assertEqual(0, f_sum.call_count)
        f_add_intervals.assert_called_once_with([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        f_dumps.assert_called_once_with('add_i_ret')
        ex_data_list = ex_data.get_all_data()

        self.assertEqual(1, len(ex_data_list))
        ds_info, data_drawer, info, err = ex_data_list[0]  # type: (DataSourceInfo, DataForHistogramDrawer, Info, Err)
        self.assertEqual(TestsInChart.SINGLE_TEST, ds_info.tests_in_chart)
        self.assertEqual(PValueSequence(test_id, PValuesFileType.DATA, data_num), ds_info.p_value_sequence)
        self.assertEqual('dumps_ret', data_drawer.json_data_string)
        self.assertEqual('x_label_str', data_drawer.x_label)
        self.assertEqual('y_label_str', data_drawer.y_label)
        self.assertEqual('title_str', data_drawer.title)
        self.assertEqual([], all_seqcs)

    def test_add_p_values_to_interval_random_p_values(self):
        self.extractor.add_p_values_to_interval(self.quantities, self.sample_p_values)
        self.assertEqual(self.expected_quantities, self.quantities)

    def test_add_p_values_to_interval_mid_interval(self):
        p_values = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
        expected_quantities = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.extractor.add_p_values_to_interval(self.quantities, p_values)
        self.assertEqual(expected_quantities, self.quantities)

    def test_add_p_values_to_interval_boundary(self):
        p_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        expected_quantities = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        self.extractor.add_p_values_to_interval(self.quantities, p_values)
        self.assertEqual(expected_quantities, self.quantities)

        expected_quantities = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        self.extractor.add_p_values_to_interval(self.quantities, p_values)
        self.assertEqual(expected_quantities, self.quantities)

    def test_add_intervals_to_quantities(self):
        quantities = [4, 10, 456, 1, 0, 12, 45, 97, 78, 84]
        expected = []
        for i in range(10):
            expected.append([HistogramExtractor.intervals[i], quantities[i]])
        ret = self.extractor.add_intervals_to_quantities(quantities)
        self.assertEqual(expected, ret)

    def test_sum_quantities_raises(self):
        q1 = [1, 2, 3]
        q2 = [1, 2]
        with self.assertRaises(RuntimeError) as ex:
            self.extractor.sum_quantities(q1, q2)
        self.assertEqual('Quantities do not have the same length (3, 2)', str(ex.exception))

    def test_sum_quantities(self):
        q1 = [0, 10, 54, 1, 2, 3, 45, 78, 125, 12]
        q2 = [4, 0, 0, 12, 81, 98, 123, 45, 62, 47]
        expected = [4, 10, 54, 13, 83, 101, 168, 123, 187, 59]
        self.extractor.sum_quantities(q1, q2)
        self.assertEqual(expected, q1)

    def test_get_json_data(self):
        exp = '{"columns": ["interval", "value"], ' \
               '"index": ["[0.0, 0.1)", "[0.1, 0.2)", "[0.2, 0.3)", "[0.3, 0.4)", "[0.4, 0.5)", "[0.5, 0.6)", ' \
               '"[0.6, 0.7)", "[0.7, 0.8)", "[0.8, 0.9)", "[0.9, 1.0]"], ' \
               '"data": [["[0.0, 0.1)", 0], ["[0.1, 0.2)", 1], ["[0.2, 0.3)", 1], ["[0.3, 0.4)", 1], ' \
               '["[0.4, 0.5)", 4], ["[0.5, 0.6)", 5], ["[0.6, 0.7)", 3], ["[0.7, 0.8)", 3], ' \
               '["[0.8, 0.9)", 2], ["[0.9, 1.0]", 0]]}'
        input_arr = [['[0.0, 0.1)', 0], ['[0.1, 0.2)', 1], ['[0.2, 0.3)', 1], ['[0.3, 0.4)', 1],
                     ['[0.4, 0.5)', 4], ['[0.5, 0.6)', 5], ['[0.6, 0.7)', 3], ['[0.7, 0.8)', 3],
                     ['[0.8, 0.9)', 2], ['[0.9, 1.0]', 0]]
        ret = self.extractor.get_json_data(input_arr)
        self.assertEqual(exp, ret)
