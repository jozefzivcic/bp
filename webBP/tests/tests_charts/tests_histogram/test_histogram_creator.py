from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from charts.chart_type import ChartType
from charts.charts_storage_item import ChartsStorageItem
from charts.data_source_info import DataSourceInfo
from charts.histogram.data_for_histogram_creator import DataForHistogramCreator
from charts.histogram.histogram_creator import HistogramCreator
from charts.dto.histogram_dto import HistogramDto
from charts.tests_in_chart import TestsInChart
from enums.hist_for_tests import HistForTests
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_histogram_creator')


class TestHistogramCreator(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        dto1 = PValuesDto({'results': [0.779952, 0.468925, 0.468925, 0.511232, 0.462545, 0.666913, 0.171598, 0.375557,
                                       0.746548, 0.558648]})
        dto2 = PValuesDto({'results': [0.879952, 0.568925, 0.568925, 0.611232, 0.562545, 0.766913, 0.271598, 0.475557,
                                       0.846548, 0.658648]})
        acc = PValuesAccumulator()
        acc.add(456, dto1)
        acc.add(654, dto2)

        hist_dto = HistogramDto('intervals', 'number of p-values', 'histogram', [HistForTests.ALL_TESTS,
                                                                                 HistForTests.INDIVIDUAL_TESTS])
        self.data_for_creator = DataForHistogramCreator(hist_dto, acc, working_dir, 789)
        self.creator = HistogramCreator()

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_create_p_values_chart(self):
        ch_storage = self.creator.create_histogram(self.data_for_creator)
        cs_items = ch_storage.get_all_items()
        self.assertEqual(3, len(cs_items))

        seq1 = PValueSequence(456, PValuesFileType.RESULTS)
        seq2 = PValueSequence(654, PValuesFileType.RESULTS)

        ch_item = cs_items[0]  # type: ChartsStorageItem
        ch_info = ch_item.ch_info
        self.assertTrue(TestsInChart.SINGLE_TEST, ch_info.ds_info.tests_in_chart)
        self.assertTrue(seq1, ch_info.ds_info.p_value_sequence)
        self.assertEqual(ChartType.HISTOGRAM, ch_info.chart_type)
        self.assertEqual(self.data_for_creator.file_id, ch_info.file_id)

        ch_item = cs_items[1]  # type: ChartsStorageItem
        ch_info = ch_item.ch_info
        self.assertTrue(TestsInChart.SINGLE_TEST, ch_info.ds_info.tests_in_chart)
        self.assertTrue(seq2, ch_info.ds_info.p_value_sequence)
        self.assertEqual(ChartType.HISTOGRAM, ch_info.chart_type)
        self.assertEqual(self.data_for_creator.file_id, ch_info.file_id)

        ch_item = cs_items[2]  # type: ChartsStorageItem
        ch_info = ch_item.ch_info
        self.assertTrue(TestsInChart.MULTIPLE_TESTS, ch_info.ds_info.tests_in_chart)
        self.assertTrue([seq1, seq2], ch_info.ds_info.p_value_sequence)
        self.assertEqual(ChartType.HISTOGRAM, ch_info.chart_type)
        self.assertEqual(self.data_for_creator.file_id, ch_info.file_id)

    def test_get_file_name_multiple_tests(self):
        seqcs = [PValueSequence(1, PValuesFileType.RESULTS), PValueSequence(2, PValuesFileType.DATA, 2)]
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, seqcs)
        expected = join(working_dir, 'hist_mult_t_first_tid_1.png')
        ret = self.creator.get_file_name_for_chart(working_dir, ds_info)
        self.assertEqual(expected, ret)

    def test_get_file_name_single_test_results(self):
        seq = PValueSequence(1, PValuesFileType.RESULTS)
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, seq)
        expected = join(working_dir, 'hist_single_t1')
        ret = self.creator.get_file_name_for_chart(working_dir, ds_info)
        self.assertEqual(expected, ret)

    def test_get_file_name_single_test_data(self):
        seq = PValueSequence(1, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, seq)
        expected = join(working_dir, 'hist_single_t1_data2')
        ret = self.creator.get_file_name_for_chart(working_dir, ds_info)
        self.assertEqual(expected, ret)

    def test_check_input_none_data(self):
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(None)
        self.assertEqual('Data is None', str(context.exception))

    def test_check_input_none_histogram_dto(self):
        self.data_for_creator.histogram_dto = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(self.data_for_creator)
        self.assertEqual('Histogram DTO is None', str(context.exception))

    def test_check_input_none_accumulator(self):
        self.data_for_creator.acc = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(self.data_for_creator)
        self.assertEqual('Accumulator is None', str(context.exception))

    def test_check_input_none_directory(self):
        self.data_for_creator.directory = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(self.data_for_creator)
        self.assertEqual('Directory is None', str(context.exception))

    def test_check_input_none_file_id(self):
        self.data_for_creator.file_id = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(self.data_for_creator)
        self.assertEqual('File id is None', str(context.exception))
