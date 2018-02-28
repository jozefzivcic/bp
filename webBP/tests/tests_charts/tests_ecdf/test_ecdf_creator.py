from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from charts.data_source_info import DataSourceInfo
from charts.ecdf.data_for_ecdf_creator import DataForEcdfCreator
from charts.ecdf.ecdf_creator import EcdfCreator
from charts.ecdf_dto import EcdfDto
from charts.tests_in_chart import TestsInChart
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import TestsIdData, FileIdData, dict_for_test_14, dict_for_test_13, \
    dict_for_test_41, dict_for_test_42, dict_for_test_43

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_ecdf_creator')


class TestEcdfCreator(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.creator = EcdfCreator()
        self.ecdf_dto = EcdfDto(0.5, 'ECDF', 'p-value', 'Cumulative density', 'Empirical', 'Theoretical')
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        dto_41 = PValuesDto(dict_for_test_41)
        dto_42 = PValuesDto(dict_for_test_42)
        dto_43 = PValuesDto(dict_for_test_43)
        self.acc = PValuesAccumulator()
        self.acc.add(TestsIdData.test1_id, dto_13)
        self.acc.add(TestsIdData.test2_id, dto_14)
        self.acc.add(TestsIdData.test3_id, dto_41)
        self.acc.add(TestsIdData.test4_id, dto_42)
        self.acc.add(TestsIdData.test5_id, dto_43)
        self.data_for_creator = DataForEcdfCreator(self.ecdf_dto, self.acc, working_dir, FileIdData.file1_id)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_create_ecdf_charts_one_chart(self):
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        self.ecdf_dto.sequences = [seq]
        self.creator.create_ecdf_charts(self.data_for_creator)
        expected = join(working_dir, 'ecdf_for_test_{}_results.png'.format(TestsIdData.test1_id))
        self.assertTrue(exists(expected))

    def test_create_ecdf_charts_three_charts(self):
        seq1 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 1)
        seq2 = PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS)
        seq3 = PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS)
        self.ecdf_dto.sequences = [seq1, seq2, seq3]
        self.creator.create_ecdf_charts(self.data_for_creator)
        file1 = join(working_dir, 'ecdf_for_test_{}_data_1.png'.format(TestsIdData.test3_id))
        file2 = join(working_dir, 'ecdf_for_test_{}_results.png'.format(TestsIdData.test4_id))
        file3 = join(working_dir, 'ecdf_for_test_{}_results.png'.format(TestsIdData.test5_id))
        self.assertTrue(exists(file1))
        self.assertTrue(exists(file2))
        self.assertTrue(exists(file3))

    def test_get_file_name_results(self):
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, seq)
        expected_name = 'ecdf_for_test_{}_results.png'.format(TestsIdData.test1_id)
        expected = join(working_dir, expected_name)
        ret = self.creator.get_file_name(ds_info, working_dir)
        self.assertEqual(expected, ret)

    def test_get_file_name_data(self):
        seq = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, seq)
        expected_name = 'ecdf_for_test_{}_data_2.png'.format(TestsIdData.test2_id)
        expected = join(working_dir, expected_name)
        ret = self.creator.get_file_name(ds_info, working_dir)
        self.assertEqual(expected, ret)
