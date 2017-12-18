from unittest import TestCase

from charts.p_values.data_for_chart import DataForChart


class TestDataForChart(TestCase):
    def setUp(self):
        self.data = DataForChart()

    def test_has_members(self):
        members = ['alpha', 'x_values', 'y_values', 'x_ticks_positions', 'x_ticks_labels', 'x_label', 'y_label',
                   'title']
        existing = list(vars(self.data).keys())
        self.assertEqual(sorted(members), sorted(existing))
