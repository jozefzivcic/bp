from os import makedirs
from shutil import rmtree

from os.path import dirname, abspath, join, exists
from unittest import TestCase

from charts.proportions.data_for_proportions_drawer import DataForProportionsDrawer
from charts.proportions.proportions_drawer import ProportionsDrawer

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_proportions_drawer')


class TestProportionsDrawer(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.drawer = ProportionsDrawer()

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_draw_chart(self):
        data = DataForProportionsDrawer('title', 'test', 'proportion', 0.7, 0.9, [0, 2, 5, 7], ['test0', 'test2',
                                                                                                'test5', 'test7'],
                                        [0, 1, 2, 3, 4, 5, 6, 7, 8], [0.89, 0.75, 0.8, 0.77, 0.89, 0.82, 0.83, 0.0,
                                                                      0.72], 0.75, 0.85, 0.8)
        file = join(working_dir, 'file.png')
        self.drawer.draw_chart(data, file)
        self.assertTrue(exists(file))
