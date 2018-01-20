from os import makedirs, remove
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from copy import deepcopy

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage

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
        self.chart_info.file_id = 456

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
            file = working_dir + 'file' + str(i) + '.txt'
            chart_info = ChartInfo()
            chart_info.path_to_chart = file
            chart_info.chart_type = ChartType.P_VALUES
            chart_info.file_id = i
            expected.append(deepcopy(chart_info))
            self.charts_storage.add_chart_info(chart_info)
        self.assertEqual(expected, self.charts_storage.get_all_infos())

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
