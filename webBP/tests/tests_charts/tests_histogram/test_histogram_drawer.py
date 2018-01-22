from os import makedirs
from unittest import TestCase

from os.path import exists, dirname, abspath, join

from shutil import rmtree

from charts.histogram.data_for_histogram_drawer import DataForHistogramDrawer
from charts.histogram.histogram_drawer import HistogramDrawer

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_histogram_drawer')


class TestHistogramDrawer(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.drawer = HistogramDrawer()

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_draw_chart(self):
        data = DataForHistogramDrawer()
        data.x_label = 'interval'
        data.y_label = 'number of p-values'
        data.title = 'histogram'
        data.json_data_string = '[["[0.0, 0.1)", 0], ["[0.1, 0.2)", 1], ["[0.2, 0.3)", 1], ["[0.3, 0.4)", 1],' \
                                '["[0.4, 0.5)", 4], ["[0.5, 0.6)", 5], ["[0.6, 0.7)", 3], ["[0.7, 0.8)", 3],' \
                                '["[0.8, 0.9)", 2], ["[0.9, 1.0]", 0]]'
        file = join(working_dir, 'histogram.png')
        self.drawer.draw_chart(data, file)
        self.assertTrue(exists(file))
