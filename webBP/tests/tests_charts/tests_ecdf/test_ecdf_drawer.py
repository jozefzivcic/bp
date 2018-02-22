from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from charts.ecdf.data_for_ecdf_drawer import DataForEcdfDrawer
from charts.ecdf.ecdf_drawer import EcdfDrawer
from tests.data_for_tests.common_data import dict_for_test_13

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_ecdf_drawer')


class TestEcdfDrawer(TestCase):
    def get_data(self):
        data = DataForEcdfDrawer(0.01, 'ECDF', 'p-value', 'likelihood of occurence', 'Empirical', 'Theoretical')
        return data

    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.drawer = EcdfDrawer()
        self.data = self.get_data()

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_draw_chart_few_p_values(self):
        self.data.p_values = [0.3, 0.3, 0.4, 0.4, 0.7]
        file = join(working_dir, 'chart.png')
        self.drawer.draw_chart(self.data, file)

        self.assertTrue(exists(file))

    def test_draw_chart_more_p_values(self):
        self.data.p_values = dict_for_test_13['results']

        file = join(working_dir, 'chart.png')
        self.drawer.draw_chart(self.data, file)

        self.assertTrue(exists(file))
