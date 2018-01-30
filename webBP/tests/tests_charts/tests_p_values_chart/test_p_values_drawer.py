from filecmp import cmp
from itertools import repeat
from os import makedirs
from os.path import dirname, abspath, join, exists, isfile
from unittest import TestCase

from shutil import rmtree
from unittest.mock import patch

from charts.p_values.data_for_p_values_drawer import DataForPValuesDrawer
from charts.p_values.p_values_drawer import PValuesDrawer
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_p_values_drawer')


class TestPValuesDrawer(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.drawer = PValuesDrawer()
        self.data = self.get_data()

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_create_some_file(self):
        file = join(working_dir, 'graph.png')
        self.drawer.draw_chart(self.data, file)
        self.assertTrue(isfile(file))

    def test_create_zoomed_graph(self):
        self.data.y_axis_ticks = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.05]
        self.data.y_axis_labels = ['0.0', '0.00001', '0.0001', '0.001', '0.01', '0.05']
        file = join(working_dir, 'graph.png')
        self.drawer.draw_chart(self.data, file)
        self.assertTrue(isfile(file))

    def test_create_two_same_graphs(self):
        file_1 = join(working_dir, 'graph1.png')
        file_2 = join(working_dir, 'graph2.png')
        self.drawer.draw_chart(self.data, file_1)
        self.drawer.draw_chart(self.data, file_2)
        self.assertTrue(isfile(file_1))
        self.assertTrue(isfile(file_2))
        self.assertTrue(cmp(file_1, file_2))

    @patch('matplotlib.pyplot.ylim')
    def test_assert_called_ylim_not_zoomed(self, func):
        self.data.zoomed = False
        file = join(working_dir, 'graph.png')
        self.drawer.draw_chart(self.data, file)
        func.assert_called_once_with((0.000001, 1.0))

    @patch('matplotlib.pyplot.ylim')
    def test_assert_called_ylim_zoomed(self, func):
        self.data.zoomed = True
        self.data.y_axis_ticks = [0.000001, 0.00001, 0.0001]
        file = join(working_dir, 'graph.png')
        self.drawer.draw_chart(self.data, file)
        func.assert_called_once_with((0.000001, 0.0001))

    @patch('matplotlib.pyplot.axhline')
    def test_assert_called_axhline_when_not_zoomed(self, func):
        self.data.zoomed = False
        file = join(working_dir, 'graph.png')
        self.drawer.draw_chart(self.data, file)
        func.assert_called_once_with(y=self.data.alpha, color='r', linestyle='--')

    @patch('matplotlib.pyplot.axhline')
    def test_assert_not_called_axhline_when_zoomed(self, func):
        self.data.zoomed = True
        file = join(working_dir, 'graph.png')
        self.drawer.draw_chart(self.data, file)
        self.assertFalse(func.called)

    def get_data(self):
        data = DataForPValuesDrawer()

        data.x_values = list(repeat(1, 10))
        data.x_values.extend(repeat(2, 10))
        data.x_values.extend(repeat(3, 10))

        data.y_values = list(dict_for_test_13['results'])
        data.y_values.extend(list(dict_for_test_14['data1']))
        data.y_values.extend(list(dict_for_test_14['data2']))

        data.x_ticks_positions = [1, 2, 3]

        data.x_ticks_labels = ['Frequency', 'Cumulative Sums_1', 'Cumulative Sums_2']

        data.y_axis_ticks = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0]
        data.y_axis_labels = ['0.0', '0.00001', '0.0001', '0.001', '0.01', '0.1', '1.0']

        data.x_label = 'test'

        data.y_label = 'p-value'

        data.title = 'p-values from selected tests'

        return data
