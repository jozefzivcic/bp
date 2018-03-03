from os import makedirs
from os.path import dirname, abspath, join, exists
from shutil import rmtree
from unittest import TestCase
from unittest.mock import MagicMock

from charts.chart_type import ChartType
from charts.p_values.data_for_p_values_creator import DataForPValuesCreator
from charts.p_values.p_values_creator import PValuesCreator
from charts.dto.p_values_chart_dto import PValuesChartDto
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, dict_for_test_41, TestsIdData, \
    FileIdData
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_p_values_creator')


class TestPValuesCreator(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)

        self.test1_id = TestsIdData.test1_id
        self.test2_id = TestsIdData.test2_id
        self.test3_id = TestsIdData.test3_id
        self.file1_id = FileIdData.file1_id


        config_storage = MagicMock()
        config_storage.nist = 'nist'
        self.p_values_creator = PValuesCreator(None, config_storage)

        self.p_values_chart_dto = PValuesChartDto(0.01, 'tests', 'p-value', 'p-values chart')
        acc = PValuesAccumulator()
        dto = PValuesDto(dict_for_test_13)
        acc.add(self.test1_id, dto)
        dto = PValuesDto(dict_for_test_14)
        acc.add(self.test2_id, dto)
        dto = PValuesDto(dict_for_test_41)
        acc.add(self.test3_id, dto)
        self.data_for_p_values_creator = DataForPValuesCreator(self.p_values_chart_dto, acc, working_dir, self.file1_id)

        self.p_values_creator._extractor._test_dao.get_test_by_id = MagicMock(side_effect=db_test_dao_get_test_by_id)
        self.p_values_creator._extractor._nist_dao.get_nist_param_for_test = \
            MagicMock(side_effect=nist_dao_get_nist_param_for_test)

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

    def test_get_file_name_not_zoomed(self):
        file_name = 'p_values_for_file_' + str(self.data_for_p_values_creator.file_id) + '.png'
        expected = join(working_dir, file_name)
        ret = self.p_values_creator.get_file_name_for_p_values_chart(self.data_for_p_values_creator)
        self.assertEqual(expected, ret)

    def test_get_file_name_zoomed(self):
        self.data_for_p_values_creator.chart_options.zoomed = True
        file_name = 'p_values_for_file_' + str(self.data_for_p_values_creator.file_id) + '_zoomed.png'
        expected = join(working_dir, file_name)
        ret = self.p_values_creator.get_file_name_for_p_values_chart(self.data_for_p_values_creator)
        self.assertEqual(expected, ret)

    def test_create_p_values_chart(self):
        chart_info = self.p_values_creator.create_p_values_chart(self.data_for_p_values_creator)
        self.assertTrue(exists(chart_info.path_to_chart))
        self.assertEqual(ChartType.P_VALUES, chart_info.chart_type)
        self.assertEqual(chart_info.file_id, self.data_for_p_values_creator.file_id)

    def test_create_zoomed_p_values_chart(self):
        self.data_for_p_values_creator.chart_options.zoomed = True
        chart_info = self.p_values_creator.create_p_values_chart(self.data_for_p_values_creator)
        self.assertTrue(exists(chart_info.path_to_chart))
        self.assertEqual(ChartType.P_VALUES_ZOOMED, chart_info.chart_type)
        self.assertEqual(chart_info.file_id, self.data_for_p_values_creator.file_id)
