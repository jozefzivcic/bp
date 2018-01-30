from unittest import TestCase

from charts.p_values.data_for_p_values_drawer import DataForPValuesDrawer


class TestDataForChart(TestCase):
    def setUp(self):
        self.data = DataForPValuesDrawer()

    def test_has_members(self):
        members = ['alpha', 'x_values', 'y_values', 'x_ticks_positions', 'x_ticks_labels', 'y_axis_ticks',
                   'y_axis_labels', 'x_label', 'y_label', 'title', 'zoomed']
        existing = list(vars(self.data).keys())
        self.assertEqual(sorted(members), sorted(existing))
