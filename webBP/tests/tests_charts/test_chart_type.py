from unittest import TestCase

from charts.chart_type import ChartType


class TestChartType(TestCase):
    def test_comparisons(self):
        self.assertTrue(ChartType.P_VALUES < ChartType.P_VALUES_ZOOMED)
        self.assertTrue(ChartType.P_VALUES < ChartType.HISTOGRAM)
        self.assertTrue(ChartType.P_VALUES < ChartType.TESTS_DEPENDENCY)
        self.assertTrue(ChartType.P_VALUES < ChartType.ECDF)
        self.assertTrue(ChartType.P_VALUES < ChartType.BOXPLOT_PT)
        self.assertTrue(ChartType.P_VALUES < ChartType.PROPORTIONS)

        self.assertTrue(ChartType.P_VALUES_ZOOMED < ChartType.HISTOGRAM)
        self.assertTrue(ChartType.P_VALUES_ZOOMED < ChartType.TESTS_DEPENDENCY)
        self.assertTrue(ChartType.P_VALUES_ZOOMED < ChartType.ECDF)
        self.assertTrue(ChartType.P_VALUES_ZOOMED < ChartType.BOXPLOT_PT)
        self.assertTrue(ChartType.P_VALUES_ZOOMED < ChartType.PROPORTIONS)

        self.assertTrue(ChartType.HISTOGRAM < ChartType.TESTS_DEPENDENCY)
        self.assertTrue(ChartType.HISTOGRAM < ChartType.ECDF)
        self.assertTrue(ChartType.HISTOGRAM < ChartType.BOXPLOT_PT)
        self.assertTrue(ChartType.HISTOGRAM < ChartType.PROPORTIONS)

        self.assertTrue(ChartType.TESTS_DEPENDENCY < ChartType.ECDF)
        self.assertTrue(ChartType.TESTS_DEPENDENCY < ChartType.BOXPLOT_PT)
        self.assertTrue(ChartType.TESTS_DEPENDENCY < ChartType.PROPORTIONS)

        self.assertTrue(ChartType.ECDF < ChartType.BOXPLOT_PT)
        self.assertTrue(ChartType.ECDF < ChartType.PROPORTIONS)

        self.assertTrue(ChartType.BOXPLOT_PT < ChartType.PROPORTIONS)