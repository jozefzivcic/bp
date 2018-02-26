from os import makedirs, remove
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from copy import deepcopy

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import FileIdData

this_dir = dirname(abspath(__file__))
working_dir = abspath(join(this_dir, 'working_dir_charts_storage'))


class TestPathStorage(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.charts_storage = ChartsStorage()

        self.chart_info = ChartInfo()
        self.chart_info.path_to_chart = '/home/path/to/file.txt'
        self.chart_info.chart_type = ChartType.P_VALUES
        self.chart_info.file_id = FileIdData.file1_id

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_add_none_chart_info(self):
        with self.assertRaises(TypeError) as context:
            self.charts_storage.add_chart_info(None)
        self.assertEqual('Chart info is None', str(context.exception))

    def test_add_none_path(self):
        self.chart_info.path_to_chart = None
        with self.assertRaises(TypeError) as context:
            self.charts_storage.add_chart_info(self.chart_info)
        self.assertEqual('Path to chart is None', str(context.exception))

    def test_add_none_chart_type(self):
        self.chart_info.chart_type= None
        with self.assertRaises(TypeError) as context:
            self.charts_storage.add_chart_info(self.chart_info)
        self.assertEqual('Chart type is None', str(context.exception))

    def test_add_none_file_id(self):
        self.chart_info.file_id = None
        with self.assertRaises(TypeError) as context:
            self.charts_storage.add_chart_info(self.chart_info)
        self.assertEqual('file_id in chart_info is None', str(context.exception))

    def test_add_one_path(self):
        self.charts_storage.add_chart_info(self.chart_info)
        self.assertEqual([deepcopy(self.chart_info)], self.charts_storage.get_all_infos())

    def test_add_more_paths(self):
        expected = []
        for i in range(0, 10):
            file = join(working_dir, 'file' + str(i) + '.txt')
            chart_info = ChartInfo()
            chart_info.path_to_chart = file
            chart_info.chart_type = ChartType.P_VALUES
            chart_info.file_id = i
            expected.append(deepcopy(chart_info))
            self.charts_storage.add_chart_info(chart_info)
        self.assertEqual(expected, self.charts_storage.get_all_infos())

    def test_extend(self):
        file = join(working_dir, 'file1000.txt')
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, PValueSequence(1000, PValuesFileType.RESULTS))
        chart_info = ChartInfo(ds_info, file, ChartType.P_VALUES_ZOOMED, 1000)
        self.charts_storage.add_chart_info(chart_info)

        expected = [chart_info]
        another_storage = ChartsStorage()

        for i in range(0, 10):
            file = join(working_dir, 'file' + str(i) + '.txt')
            chart_info = ChartInfo()
            ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, PValueSequence(i, PValuesFileType.RESULTS))
            chart_info.ds_info = ds_info
            chart_info.path_to_chart = file
            chart_info.chart_type = ChartType.HISTOGRAM
            chart_info.file_id = i
            expected.append(deepcopy(chart_info))
            another_storage.add_chart_info(chart_info)

        self.assertEqual(expected[1:], another_storage.get_all_infos())
        self.charts_storage.extend(another_storage)
        self.assertEqual(expected, self.charts_storage.get_all_infos())
        self.assertEqual([], another_storage.get_all_infos())

        another_storage.extend(self.charts_storage)
        self.assertEqual(expected, another_storage.get_all_infos())
        self.assertEqual([], self.charts_storage.get_all_infos())

    def test_delete_files_on_paths(self):
        expected = []
        for i in range(0, 10):
            file = join(working_dir, 'file' + str(i) + '.txt')
            chart_info = ChartInfo()
            chart_info.path_to_chart = file
            chart_info.chart_type = ChartType.P_VALUES
            chart_info.file_id = i
            expected.append(deepcopy(chart_info))
            self.charts_storage.add_chart_info(chart_info)
            open(file, 'a').close()
            self.assertTrue(exists(file))
        remove(join(working_dir, 'file5.txt'))

        self.charts_storage.delete_files_on_paths()

        for i in range(0, 5):
            file = join(working_dir, 'file' + str(i) + '.txt')
            self.assertFalse(exists(file))
        for i in range(6, 10):
            file = join(working_dir, 'file' + str(i) + '.txt')
            self.assertFalse(exists(file))
