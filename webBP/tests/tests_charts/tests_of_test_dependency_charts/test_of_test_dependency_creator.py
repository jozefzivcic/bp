from os import makedirs, listdir
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree
from unittest.mock import MagicMock, patch

from copy import deepcopy

from charts.chart_type import ChartType
from charts.extracted_data import ExtractedData
from charts.test_dependency.data_for_test_dependency_creator import DataForTestDependencyCreator
from charts.test_dependency.data_for_test_dependency_drawer import DataForTestDependencyDrawer
from charts.test_dependency.test_dependency_creator import TestDependencyCreator
from charts.dto.test_dependency_dto import TestDependencyDto
from common.info.test_dep_filtered_info import TestDepFilteredInfo
from common.info.test_dep_unif_info import TestDepUnifInfo
from enums.filter_uniformity import FilterUniformity
from enums.test_dep_pairs import TestDepPairs
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_accumulator import SequenceAccumulator
from tests.data_for_tests.common_data import TestsIdData, dict_for_test_43, dict_for_test_13, dict_for_test_14, \
    dict_for_test_41, dict_for_test_42, FileIdData
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test, \
    func_return_false, func_return_true

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_test_dependency_creator')


class TestOfTestDependencyCreator(TestCase):
    def mock_func(self, func_name, side_effect):
        patcher = patch(func_name, side_effect=side_effect)
        self.addCleanup(patcher.stop)
        patcher.start()

    def mock(self):
        self.mock_func('managers.dbtestmanager.DBTestManager.get_test_by_id', db_test_dao_get_test_by_id)
        self.mock_func('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                       nist_dao_get_nist_param_for_test)

    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.mock()
        self.config_storage = MagicMock(nist='nist')
        self.creator = TestDependencyCreator(None, self.config_storage)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_create_test_dependency_charts_none_data(self):
        with self.assertRaises(TypeError) as context:
            self.creator.create_test_dependency_charts(None)
        self.assertEqual('Input data is None', str(context.exception))

    @patch('common.unif_check.UnifCheck.check_for_uniformity', side_effect=func_return_true)
    @patch('common.unif_check.UnifCheck.is_approx_fulfilled', return_value=True)
    def test_create_test_dependency_charts_no_chart(self, func_is_approx, func_check_unif):
        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS))

        p_values_dto_for_test1 = PValuesDto(dict_for_test_13)

        p_values_acc = PValuesAccumulator()
        p_values_acc.add(TestsIdData.test1_id, p_values_dto_for_test1)

        dependency_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_NON_UNIFORM, seq_acc,
                                           'Dependency of two tests')
        data_for_creator = DataForTestDependencyCreator(dependency_dto, p_values_acc, working_dir, FileIdData.file1_id)
        storage = self.creator.create_test_dependency_charts(data_for_creator)

        cs_item_list = storage.get_all_items()
        self.assertEqual(0, len(cs_item_list))
        num_of_files = len(listdir(working_dir))
        self.assertEqual(0, num_of_files)

    @patch('common.unif_check.UnifCheck.check_for_uniformity', side_effect=func_return_true)
    @patch('common.unif_check.UnifCheck.get_p_value', return_value=0.5)
    @patch('common.unif_check.UnifCheck.is_approx_fulfilled', return_value=True)
    def test_create_test_dependency_charts_one_chart(self, func_is_approx, func_get, func_check_unif):
        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1))

        p_values_dto_for_test1 = PValuesDto(dict_for_test_13)
        p_values_dto_for_test2 = PValuesDto(dict_for_test_14)

        p_values_acc = PValuesAccumulator()
        p_values_acc.add(TestsIdData.test1_id, p_values_dto_for_test1)
        p_values_acc.add(TestsIdData.test2_id, p_values_dto_for_test2)

        dependency_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_UNIFORM, seq_acc,
                                           'Dependency of two tests')
        data_for_creator = DataForTestDependencyCreator(dependency_dto, p_values_acc, working_dir, FileIdData.file1_id)
        storage = self.creator.create_test_dependency_charts(data_for_creator)

        cs_item_list = storage.get_all_items()
        chart_info = cs_item_list[0].ch_info
        self.assertEqual(1, len(cs_item_list))
        self.assertTrue(exists(chart_info.path_to_chart))
        self.assertEqual(ChartType.TESTS_DEPENDENCY, chart_info.chart_type)
        self.assertEqual(FileIdData.file1_id, chart_info.file_id)
        num_of_files = len(listdir(working_dir))
        self.assertEqual(1, num_of_files)

    @patch('common.unif_check.UnifCheck.check_for_uniformity', side_effect=func_return_true)
    @patch('common.unif_check.UnifCheck.get_p_value', return_value=0.5)
    @patch('common.unif_check.UnifCheck.is_approx_fulfilled', return_value=True)
    def test_create_test_dependency_charts_ten_charts(self, func_is_approx, func_get, func_check):
        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS))

        p_values_dto_for_test1 = PValuesDto(dict_for_test_13)
        p_values_dto_for_test2 = PValuesDto(dict_for_test_14)
        p_values_dto_for_test3 = PValuesDto(dict_for_test_41)
        p_values_dto_for_test4 = PValuesDto(dict_for_test_42)
        p_values_dto_for_test5 = PValuesDto(dict_for_test_43)

        p_values_acc = PValuesAccumulator()
        p_values_acc.add(TestsIdData.test1_id, p_values_dto_for_test1)
        p_values_acc.add(TestsIdData.test2_id, p_values_dto_for_test2)
        p_values_acc.add(TestsIdData.test3_id, p_values_dto_for_test3)
        p_values_acc.add(TestsIdData.test4_id, p_values_dto_for_test4)
        p_values_acc.add(TestsIdData.test5_id, p_values_dto_for_test5)

        dependency_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_UNIFORM, seq_acc,
                                           'Dependency of two tests')
        data_for_creator = DataForTestDependencyCreator(dependency_dto, p_values_acc, working_dir, FileIdData.file1_id)
        storage = self.creator.create_test_dependency_charts(data_for_creator)

        cs_item_list = storage.get_all_items()
        self.assertEqual(10, len(cs_item_list))
        for cs_item in cs_item_list:
            chart_info = cs_item.ch_info
            self.assertTrue(exists(chart_info.path_to_chart))
            self.assertEqual(ChartType.TESTS_DEPENDENCY, chart_info.chart_type)
            self.assertEqual(FileIdData.file1_id, chart_info.file_id)

        num_of_files = len(listdir(working_dir))
        self.assertEqual(10, num_of_files)

    @patch('common.unif_check.UnifCheck.check_for_uniformity', side_effect=func_return_true)
    @patch('common.unif_check.UnifCheck.get_p_value', return_value=0.5)
    @patch('common.unif_check.UnifCheck.is_approx_fulfilled', return_value=True)
    def test_create_test_dependency_charts_filter_out_sub_tests(self, func_is_approx, func_get, func_check):
        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2))

        p_values_dto_for_test1 = PValuesDto(dict_for_test_13)
        p_values_dto_for_test2 = PValuesDto(dict_for_test_14)
        p_values_dto_for_test3 = PValuesDto(dict_for_test_41)
        p_values_dto_for_test4 = PValuesDto(dict_for_test_42)
        p_values_dto_for_test5 = PValuesDto(dict_for_test_43)

        p_values_acc = PValuesAccumulator()
        p_values_acc.add(TestsIdData.test1_id, p_values_dto_for_test1)
        p_values_acc.add(TestsIdData.test2_id, p_values_dto_for_test2)
        p_values_acc.add(TestsIdData.test3_id, p_values_dto_for_test3)
        p_values_acc.add(TestsIdData.test4_id, p_values_dto_for_test4)
        p_values_acc.add(TestsIdData.test5_id, p_values_dto_for_test5)

        dependency_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_UNIFORM, seq_acc,
                                           'Dependency of two tests', TestDepPairs.SKIP_PAIRS_FROM_SUBTESTS)
        data_for_creator = DataForTestDependencyCreator(dependency_dto, p_values_acc, working_dir, FileIdData.file1_id)
        storage = self.creator.create_test_dependency_charts(data_for_creator)

        cs_item_list = storage.get_all_items()
        self.assertEqual(8, len(cs_item_list))
        for cs_item in cs_item_list:
            chart_info = cs_item.ch_info
            self.assertTrue(exists(chart_info.path_to_chart))
            self.assertEqual(ChartType.TESTS_DEPENDENCY, chart_info.chart_type)
            self.assertEqual(FileIdData.file1_id, chart_info.file_id)

        num_of_files = len(listdir(working_dir))
        self.assertEqual(8, num_of_files)

    @patch('p_value_processing.sequence_pairs.SequencePairs.should_remove')
    def test_create_test_dependency_charts_extracted_data(self, f_remove):
        def side_eff_mock(check_obj, seq1, seq2, filter_unif):
            if seq1[0] < 0.5:
                return True, 0.5, True
            else:
                return False, 0.6, True
        f_remove.side_effect = side_eff_mock

        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS))

        p_values_dto_for_test1 = PValuesDto(dict_for_test_13)
        p_values_dto_for_test2 = PValuesDto(dict_for_test_14)
        p_values_dto_for_test3 = PValuesDto(dict_for_test_41)
        p_values_dto_for_test4 = PValuesDto(dict_for_test_42)
        p_values_dto_for_test5 = PValuesDto(dict_for_test_43)

        p_values_acc = PValuesAccumulator()
        p_values_acc.add(TestsIdData.test1_id, p_values_dto_for_test1)
        p_values_acc.add(TestsIdData.test2_id, p_values_dto_for_test2)
        p_values_acc.add(TestsIdData.test3_id, p_values_dto_for_test3)
        p_values_acc.add(TestsIdData.test4_id, p_values_dto_for_test4)
        p_values_acc.add(TestsIdData.test5_id, p_values_dto_for_test5)

        dependency_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_UNIFORM, seq_acc,
                                           'Dependency of two tests')
        data_for_creator = DataForTestDependencyCreator(dependency_dto, p_values_acc, working_dir, FileIdData.file1_id)
        storage = self.creator.create_test_dependency_charts(data_for_creator)
        for cs_item in storage.get_all_items():
            info = cs_item.info
            expected = TestDepUnifInfo(0.6, True)
            self.assertEqual(expected, info)
        infos = storage.get_infos_for_chart_type(ChartType.TESTS_DEPENDENCY)
        self.assertEqual(1, len(infos))
        expected = TestDepFilteredInfo(1, 10, FilterUniformity.REMOVE_UNIFORM)
        self.assertEqual(expected, infos[0])

    @patch('charts.test_dependency.test_dependency_extractor.TestDependencyExtractor.get_data_from_accumulator')
    def test_errs_propagated(self, f_get_data):
        ex_data = ExtractedData()
        err1 = MagicMock(error='This is first error')
        err2 = MagicMock(error='This is second error')
        ex_data.add_err(err1)
        ex_data.add_err(err2)
        f_get_data.return_value = ex_data
        dependency_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_UNIFORM, SequenceAccumulator(),
                                           'Dependency of two tests')
        data_for_creator = DataForTestDependencyCreator(dependency_dto, PValuesAccumulator(), working_dir,
                                                        FileIdData.file1_id)
        storage = self.creator.create_test_dependency_charts(data_for_creator)
        ret = storage.get_errors_for_chart_type(ChartType.TESTS_DEPENDENCY)
        expected = [deepcopy(err1), deepcopy(err2)]
        self.assertEqual(expected, ret)

    def test_get_file_name(self):
        data = DataForTestDependencyDrawer([0.4, 0.5, 0.6], [0.6, 0.4, 0.5], 'title', 'x_label', 'y_label')
        expected = join(working_dir, 'dependency_of_' + data.x_label + '_and_' + data.y_label + '.png')
        ret = self.creator.get_file_name(working_dir, data)
        self.assertEqual(expected, ret)

    def test_get_file_name_replace_spaces(self):
        data = DataForTestDependencyDrawer([0.4, 0.5, 0.6], [0.6, 0.4, 0.5], 'title', 'x_label and', 'y label')
        expected = join(working_dir, 'dependency_of_x_label_and_and_y_label.png')
        ret = self.creator.get_file_name(working_dir, data)
        self.assertEqual(expected, ret)
