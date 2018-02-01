from filecmp import cmp
from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from copy import deepcopy

from charts.test_dependency.data_for_test_dependency_drawer import DataForTestDependencyDrawer
from charts.test_dependency.test_dependency_drawer import TestDependencyDrawer
from tests.data_for_tests.common_data import dict_for_test_42, dict_for_test_43


this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_test_dependency_drawer')


class TestOfTestDependencyDrawer(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.drawer = TestDependencyDrawer()
        self.data_for_drawer = DataForTestDependencyDrawer(dict_for_test_42['results'], dict_for_test_43['results'],
                                                           'Dependency of two tests', 'Test_4', 'Test_5')

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_draw_chart(self):
        file_name = join(working_dir, 'dependency_chart.png')
        self.drawer.draw_chart(self.data_for_drawer, file_name)
        self.assertTrue(exists(file_name))

    def test_draw_two_same_charts(self):
        file_name1 = join(working_dir, 'dependency_chart1.png')
        file_name2 = join(working_dir, 'dependency_chart2.png')
        self.drawer.draw_chart(self.data_for_drawer, file_name1)
        new_data = deepcopy(self.data_for_drawer)
        self.drawer.draw_chart(new_data, file_name2)

        self.assertTrue(exists(file_name1))
        self.assertTrue(exists(file_name2))
        self.assertTrue(cmp(file_name1, file_name2))
