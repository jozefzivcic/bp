from unittest import TestCase

from copy import deepcopy

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType


class TestChartInfo(TestCase):
    def setUp(self):
        self.ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, PValueSequence(1, PValuesFileType.RESULTS))

    def test_has_members(self):
        info = ChartInfo()
        members = ['ds_info', 'path_to_chart', 'chart_type', 'file_id']
        existing = list(vars(info).keys())
        self.assertEqual(sorted(members), sorted(existing))

    def test_are_equal(self):
        info1 = ChartInfo(self.ds_info, 'path', ChartType.P_VALUES, 5)
        info2 = ChartInfo(self.ds_info, 'path', ChartType.P_VALUES, 5)
        self.assertEqual(info1, info2)

    def test_are_not_equal_different_ds_info(self):
        ds2 = deepcopy(self.ds_info)
        ds2.tests_in_chart = TestsInChart.MULTIPLE_TESTS
        info1 = ChartInfo(self.ds_info, 'path', ChartType.P_VALUES, 5)
        info2 = ChartInfo(ds2, 'path', ChartType.P_VALUES, 5)
        self.assertNotEqual(info1, info2)

    def test_are_not_equal_different_path(self):
        info1 = ChartInfo(self.ds_info, 'path', ChartType.P_VALUES, 5)
        info2 = ChartInfo(self.ds_info, 'path2', ChartType.P_VALUES, 5)
        self.assertNotEqual(info1, info2)

    def test_are_not_equal_different_chart_type(self):
        info1 = ChartInfo(self.ds_info, 'path', ChartType.P_VALUES, 5)
        info2 = ChartInfo(self.ds_info, 'path', ChartType.P_VALUES_ZOOMED, 5)
        self.assertNotEqual(info1, info2)

    def test_are_not_equal_different_file_id(self):
        info1 = ChartInfo(self.ds_info, 'path', ChartType.P_VALUES, 5)
        info2 = ChartInfo(self.ds_info, 'path', ChartType.P_VALUES, 6)
        self.assertNotEqual(info1, info2)

    def test_are_not_equal_other_object(self):
        info = ChartInfo(self.ds_info, 'path', ChartType.P_VALUES, 5)
        self.assertNotEqual(info, 1)

