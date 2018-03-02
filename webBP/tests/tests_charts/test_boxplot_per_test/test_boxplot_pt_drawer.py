import json
from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from charts.boxplot_per_test.boxplot_pt_drawer import BoxplotPTDrawer
from charts.boxplot_per_test.data_for_boxplot_pt_drawer import DataForBoxplotPTDrawer

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_boxplot_pt_drawer')


class TestBoxplotPTDrawer(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.drawer = BoxplotPTDrawer()

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_draw_boxplot(self):
        data_dict = {'First test': [1, 2, 3, 4], 'Second test': [2, 3, 4, 5], 'Third test': [0, 1, 2, 3]}
        data_str = json.dumps(data_dict)
        drawer_data = DataForBoxplotPTDrawer('Boxplot per test', data_str)
        file_name = join(working_dir, 'chart.png')
        self.drawer.draw_chart(drawer_data, file_name)
        self.assertTrue(exists(file_name))

    def test_draw_thirty_charts(self):
        """
        The reason for this test is, if drawer releases resources correctly.
        If not some warning in output should appear.
        """
        iterations = 30
        for i in range(0, iterations):
            data_dict = {'First test': [1 + i, 2 + i, 3 + i, 4 + i], 'Second test': [2 + i, 3 + i, 4 + i, 5 + i],
                         'Third test': [0 + i, 1 + i, 2 + i, 3 + i]}
            data_str = json.dumps(data_dict)
            drawer_data = DataForBoxplotPTDrawer('Boxplot per test', data_str)
            file_name = join(working_dir, 'chart_{}.png'.format(i))
            self.drawer.draw_chart(drawer_data, file_name)

        for i in range(iterations):
            file_name = join(working_dir, 'chart_{}.png'.format(i))
            self.assertTrue(exists(file_name))
