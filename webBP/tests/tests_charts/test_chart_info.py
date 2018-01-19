from unittest import TestCase

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType


class TestChartInfo(TestCase):
    def test_has_members(self):
        info = ChartInfo()
        members = ['path_to_chart', 'chart_type', 'file_id']
        existing = list(vars(info).keys())
        self.assertEqual(sorted(members), sorted(existing))

    def test_are_equal(self):
        info1 = ChartInfo('path', ChartType.P_VALUES, 5)
        info2 = ChartInfo('path', ChartType.P_VALUES, 5)
        self.assertEqual(info1, info2)

    def test_are_not_equal(self):
        info1 = ChartInfo('path', ChartType.P_VALUES, 5)
        info2 = ChartInfo('path2', ChartType.P_VALUES, 5)
        self.assertNotEqual(info1, info2)

    def test_are_not_equal_other_object(self):
        info = ChartInfo('path', ChartType.P_VALUES, 5)
        self.assertNotEqual(info, 1)

