from os import makedirs
from shutil import rmtree
from unittest.mock import patch, MagicMock

from os.path import dirname, abspath, join, exists
from unittest import TestCase

from charts.chart_type import ChartType
from charts.charts_storage_item import ChartsStorageItem
from charts.dto.proportions_dto import ProportionsDto
from charts.proportions.data_for_proportions_creator import DatForProportionsCreator
from charts.proportions.proportions_creator import ProportionsCreator
from enums.prop_formula import PropFormula
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, dict_for_test_41, TestsIdData, \
    FileIdData
from tests.data_for_tests.common_functions import nist_dao_get_nist_param_for_test, db_test_dao_get_test_by_id

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_p_values_creator')


class TestProportionsCreator(TestCase):
    def mock_func(self, func_name, side_effect):
        patcher = patch(func_name, side_effect=side_effect)
        self.addCleanup(patcher.stop)
        patcher.start()

    def mock(self):
        self.mock_func('managers.dbtestmanager.DBTestManager.get_test_by_id', db_test_dao_get_test_by_id)
        self.mock_func('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                       nist_dao_get_nist_param_for_test)

    def setUp(self):
        self.mock()
        if not exists(working_dir):
            makedirs(working_dir)
        storage = MagicMock(nist='nist')
        self.creator = ProportionsCreator(None, storage)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_create_prop_charts(self):
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        dto_41 = PValuesDto(dict_for_test_41)
        acc = PValuesAccumulator()
        acc.add(TestsIdData.test1_id, dto_13)
        acc.add(TestsIdData.test2_id, dto_14)
        acc.add(TestsIdData.test3_id, dto_41)
        prop_dto = ProportionsDto(0.01, 'Proportions chart', 'tests', 'proportions', PropFormula.ORIGINAL)
        data = DatForProportionsCreator(prop_dto, acc, working_dir, FileIdData.file1_id)
        ret = self.creator.create_prop_chart(data)
        self.assertEqual(1, len(ret.get_all_items()))
        ch_storage_item = ret.get_all_items()[0]  # type: ChartsStorageItem
        self.assertIsNone(ch_storage_item.ch_info.ds_info)
        self.assertTrue(exists(ch_storage_item.ch_info.path_to_chart))
        self.assertEqual(ChartType.PROPORTIONS, ch_storage_item.ch_info.chart_type)
        self.assertEqual(FileIdData.file1_id, ch_storage_item.ch_info.file_id)

    def test_get_file_name(self):
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        dto_41 = PValuesDto(dict_for_test_41)
        acc = PValuesAccumulator()
        acc.add(TestsIdData.test1_id, dto_13)
        acc.add(TestsIdData.test2_id, dto_14)
        acc.add(TestsIdData.test3_id, dto_41)
        expected = 'prop_first_test_id_{}.png'.format(TestsIdData.test1_id)
        expected = join(working_dir, expected)
        ret = self.creator.get_file_name(working_dir, acc)
        self.assertEqual(expected, ret)
