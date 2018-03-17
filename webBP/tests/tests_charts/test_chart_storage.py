from os import makedirs, remove
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from copy import deepcopy

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.charts_storage_item import ChartsStorageItem
from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import FileIdData

this_dir = dirname(abspath(__file__))
working_dir = abspath(join(this_dir, 'working_dir_charts_storage'))


class TestChartsStorage(TestCase):
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
        cs_item = ChartsStorageItem(deepcopy(self.chart_info))
        self.assertEqual([cs_item], self.charts_storage.get_all_items())

    def test_add_more_paths(self):
        expected = []
        for i in range(0, 10):
            file = join(working_dir, 'file' + str(i) + '.txt')
            chart_info = ChartInfo()
            chart_info.path_to_chart = file
            chart_info.chart_type = ChartType.P_VALUES
            chart_info.file_id = i
            cs_item = ChartsStorageItem(deepcopy(chart_info))
            expected.append(cs_item)
            self.charts_storage.add_chart_info(chart_info)
        self.assertEqual(expected, self.charts_storage.get_all_items())

    def test_add_infos_raises(self):
        infos1 = ['info1', 'info2']
        self.charts_storage.add_infos_from_chart(ChartType.HISTOGRAM, infos1)
        infos2 = ['info3', 'info4']
        with self.assertRaises(RuntimeError) as ex:
            self.charts_storage.add_infos_from_chart(ChartType.HISTOGRAM, infos2)
        self.assertEqual('Infos for chart type ChartType.HISTOGRAM already contained', str(ex.exception))

    def test_add_infos_from_chart(self):
        infos1 = ['info1', 'info2']
        infos2 = ['info3', 'info4']
        self.charts_storage.add_infos_from_chart(ChartType.HISTOGRAM, infos1)
        ret = self.charts_storage.get_infos_for_chart_type(ChartType.HISTOGRAM)
        self.assertEqual(deepcopy(infos1), ret)

        self.charts_storage.add_infos_from_chart(ChartType.P_VALUES_ZOOMED, infos2)
        ret = self.charts_storage.get_infos_for_chart_type(ChartType.HISTOGRAM)
        self.assertEqual(deepcopy(infos1), ret)
        ret = self.charts_storage.get_infos_for_chart_type(ChartType.P_VALUES_ZOOMED)
        self.assertEqual(deepcopy(infos2), ret)

    def test_add_errors_raises(self):
        errors1 = ['error1', 'error2']
        self.charts_storage.add_errors_from_chart(ChartType.HISTOGRAM, errors1)
        errors2 = ['error3', 'error4']
        with self.assertRaises(RuntimeError) as ex:
            self.charts_storage.add_errors_from_chart(ChartType.HISTOGRAM, errors2)
        self.assertEqual('Errors for chart type ChartType.HISTOGRAM already contained', str(ex.exception))

    def test_add_errors_from_chart(self):
        errors1 = ['error1', 'error2']
        errors2 = ['error3', 'error4']
        self.charts_storage.add_errors_from_chart(ChartType.HISTOGRAM, errors1)
        ret = self.charts_storage.get_errors_for_chart_type(ChartType.HISTOGRAM)
        self.assertEqual(deepcopy(errors1), ret)

        self.charts_storage.add_errors_from_chart(ChartType.P_VALUES_ZOOMED, errors2)
        ret = self.charts_storage.get_errors_for_chart_type(ChartType.HISTOGRAM)
        self.assertEqual(deepcopy(errors1), ret)
        ret = self.charts_storage.get_errors_for_chart_type(ChartType.P_VALUES_ZOOMED)
        self.assertEqual(deepcopy(errors2), ret)

    def test_extend_cs_items(self):
        file = join(working_dir, 'file1000.txt')
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, PValueSequence(1000, PValuesFileType.RESULTS))
        chart_info = ChartInfo(ds_info, file, ChartType.P_VALUES_ZOOMED, 1000)
        self.charts_storage.add_chart_info(chart_info)

        cs_item = ChartsStorageItem(deepcopy(chart_info))
        expected = [cs_item]
        another_storage = ChartsStorage()

        for i in range(0, 10):
            file = join(working_dir, 'file' + str(i) + '.txt')
            ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, PValueSequence(i, PValuesFileType.RESULTS))
            chart_info = ChartInfo(ds_info, file, ChartType.HISTOGRAM, i)
            cs_item = ChartsStorageItem(deepcopy(chart_info))
            expected.append(cs_item)
            another_storage.add_chart_info(chart_info)

        self.assertEqual(expected[1:], another_storage.get_all_items())
        self.charts_storage.extend(another_storage)
        self.assertEqual(expected, self.charts_storage.get_all_items())
        self.assertEqual([], another_storage.get_all_items())

        another_storage.extend(self.charts_storage)
        self.assertEqual(expected, another_storage.get_all_items())
        self.assertEqual([], self.charts_storage.get_all_items())

    def test_extend_infos(self):
        infos1 = ['info1', 'info2']
        infos2 = ['info3', 'info4']
        infos3 = ['info5', 'info6']
        infos4 = ['info7', 'info8']
        self.charts_storage.add_infos_from_chart(ChartType.P_VALUES, infos1)

        another_storage = ChartsStorage()
        another_storage.add_infos_from_chart(ChartType.P_VALUES_ZOOMED, infos2)
        another_storage.add_infos_from_chart(ChartType.HISTOGRAM, infos3)
        another_storage.add_infos_from_chart(ChartType.TESTS_DEPENDENCY, infos4)

        self.charts_storage.extend(another_storage)
        self.assertEqual(infos1, self.charts_storage.get_infos_for_chart_type(ChartType.P_VALUES))
        self.assertEqual(infos2, self.charts_storage.get_infos_for_chart_type(ChartType.P_VALUES_ZOOMED))
        self.assertEqual(infos3, self.charts_storage.get_infos_for_chart_type(ChartType.HISTOGRAM))
        self.assertEqual(infos4, self.charts_storage.get_infos_for_chart_type(ChartType.TESTS_DEPENDENCY))

        with self.assertRaises(KeyError) as ex:
            another_storage.get_infos_for_chart_type(ChartType.P_VALUES)

        with self.assertRaises(KeyError) as ex:
            another_storage.get_infos_for_chart_type(ChartType.P_VALUES_ZOOMED)

        with self.assertRaises(KeyError) as ex:
            another_storage.get_infos_for_chart_type(ChartType.HISTOGRAM)

        with self.assertRaises(KeyError) as ex:
            another_storage.get_infos_for_chart_type(ChartType.TESTS_DEPENDENCY)

    def test_extend_errors(self):
        errors1 = ['error1', 'error2']
        errors2 = ['error3', 'error4']
        errors3 = ['error5', 'error6']
        errors4 = ['error7', 'error8']
        self.charts_storage.add_errors_from_chart(ChartType.P_VALUES, errors1)

        another_storage = ChartsStorage()
        another_storage.add_errors_from_chart(ChartType.P_VALUES_ZOOMED, errors2)
        another_storage.add_errors_from_chart(ChartType.HISTOGRAM, errors3)
        another_storage.add_errors_from_chart(ChartType.TESTS_DEPENDENCY, errors4)

        self.charts_storage.extend(another_storage)
        self.assertEqual(errors1, self.charts_storage.get_errors_for_chart_type(ChartType.P_VALUES))
        self.assertEqual(errors2, self.charts_storage.get_errors_for_chart_type(ChartType.P_VALUES_ZOOMED))
        self.assertEqual(errors3, self.charts_storage.get_errors_for_chart_type(ChartType.HISTOGRAM))
        self.assertEqual(errors4, self.charts_storage.get_errors_for_chart_type(ChartType.TESTS_DEPENDENCY))

        with self.assertRaises(KeyError) as ex:
            another_storage.get_errors_for_chart_type(ChartType.P_VALUES)

        with self.assertRaises(KeyError) as ex:
            another_storage.get_errors_for_chart_type(ChartType.P_VALUES_ZOOMED)

        with self.assertRaises(KeyError) as ex:
            another_storage.get_errors_for_chart_type(ChartType.HISTOGRAM)

        with self.assertRaises(KeyError) as ex:
            another_storage.get_errors_for_chart_type(ChartType.TESTS_DEPENDENCY)
