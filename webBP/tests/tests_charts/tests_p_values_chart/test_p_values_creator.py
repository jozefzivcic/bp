from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase
from unittest.mock import MagicMock

from shutil import rmtree

from charts.chart_options import ChartOptions
from charts.chart_type import ChartType
from charts.p_values.data_for_p_values_creator import DataForPValuesCreator
from charts.p_values.p_values_creator import PValuesCreator
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, dict_for_test_41
from models.test import Test
from models.nistparam import NistParam

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_p_values_creator')


class TestPValuesCreator(TestCase):
    def db_test_dao_get_test_by_id(self, test_id: int) -> Test:
        test = Test()
        test.test_table = 'nist'
        if self.test1_id == test_id:
            test.id = self.test1_id
            test.file_id = self.file1_id
            return test
        if self.test2_id == test_id:
            test.id = self.test2_id
            test.file_id = self.file1_id
            return test
        if self.test3_id == test_id:
            test.id = self.test3_id
            test.file_id = self.file1_id
            return test
        return None

    def nist_dao_get_nist_param_for_test(self, test: Test) -> NistParam:
        param = NistParam()
        if self.test1_id == test.id:
            param.test_number = 1
            return param
        if self.test2_id == test.id:
            param.test_number = 3
            return param
        if self.test3_id == test.id:
            param.test_number = 14
            return param
        return None

    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)

        self.test1_id = 13
        self.test2_id = 14
        self.test3_id = 41
        self.file1_id = 456


        config_storage = MagicMock()
        config_storage.nist = 'nist'
        self.p_values_creator = PValuesCreator(None, config_storage)

        self.chart_options = ChartOptions(0.01, 'tests', 'p-value', 'p-values chart')
        acc = PValuesAccumulator()
        dto = PValuesDto(dict_for_test_13)
        acc.add(self.test1_id, dto)
        dto = PValuesDto(dict_for_test_14)
        acc.add(self.test2_id, dto)
        dto = PValuesDto(dict_for_test_41)
        acc.add(self.test3_id, dto)
        self.data_for_p_values_creator = DataForPValuesCreator(self.chart_options, acc, working_dir, self.file1_id)

        self.p_values_creator._extractor._test_dao.get_test_by_id = MagicMock(side_effect=
                                                                              self.db_test_dao_get_test_by_id)
        self.p_values_creator._extractor._nist_dao.get_nist_param_for_test = \
            MagicMock(side_effect=self.nist_dao_get_nist_param_for_test)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_create_p_values_chart_none_data(self):
        with self.assertRaises(TypeError) as context:
            self.p_values_creator.create_p_values_chart(None)
        self.assertEqual('Data cannot be None', str(context.exception))

    def test_create_p_values_chart_none_options(self):
        self.data_for_p_values_creator.chart_options = None
        with self.assertRaises(TypeError) as context:
            self.p_values_creator.create_p_values_chart(self.data_for_p_values_creator)
        self.assertEqual('Chart options cannot be None', str(context.exception))

    def test_create_p_values_chart_none_accumulator(self):
        self.data_for_p_values_creator.acc = None
        with self.assertRaises(TypeError) as context:
            self.p_values_creator.create_p_values_chart(self.data_for_p_values_creator)
        self.assertEqual('Accumulator cannot be None', str(context.exception))

    def test_create_p_values_chart_none_directory(self):
        self.data_for_p_values_creator.directory = None
        with self.assertRaises(TypeError) as context:
            self.p_values_creator.create_p_values_chart(self.data_for_p_values_creator)
        self.assertEqual('Directory cannot be None', str(context.exception))

    def test_create_p_values_chart_none_file_id(self):
        self.data_for_p_values_creator.file_id = None
        with self.assertRaises(TypeError) as context:
            self.p_values_creator.create_p_values_chart(self.data_for_p_values_creator)
        self.assertEqual('file_id cannot be None', str(context.exception))

    def test_create_p_values_chart(self):
        chart_info = self.p_values_creator.create_p_values_chart(self.data_for_p_values_creator)
        self.assertTrue(exists(chart_info.path_to_chart))
        self.assertEqual(ChartType.P_VALUES, chart_info.chart_type)
        self.assertEqual(chart_info.file_id, self.data_for_p_values_creator.file_id)
