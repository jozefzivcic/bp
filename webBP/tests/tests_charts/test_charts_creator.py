from os import makedirs
from os.path import dirname, abspath, join, exists
from shutil import rmtree
from unittest import TestCase
from unittest.mock import MagicMock, patch

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_creator import ChartsCreator
from charts.charts_error import ChartsError
from charts.charts_storage_item import ChartsStorageItem
from charts.data_source_info import DataSourceInfo
from charts.dto.boxplot_pt_dto import BoxplotPTDto
from charts.dto.ecdf_dto import EcdfDto
from charts.dto.proportions_dto import ProportionsDto
from charts.generate_charts_dto import GenerateChartsDto
from charts.dto.histogram_dto import HistogramDto
from charts.dto.p_values_chart_dto import PValuesChartDto
from charts.dto.test_dependency_dto import TestDependencyDto
from charts.different_num_of_pvals_error import DifferentNumOfPValsError
from charts.tests_in_chart import TestsInChart
from common.error.prop_diff_len_err import PropDiffLenErr
from enums.filter_uniformity import FilterUniformity
from enums.prop_formula import PropFormula
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_accumulator import SequenceAccumulator
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, dict_for_test_41, dict_for_test_42, \
    dict_for_test_43, TestsIdData, FileIdData, short_names_dict
from tests.data_for_tests.common_functions import results_dao_get_paths_for_test_ids, db_test_dao_get_tests_by_id_list, \
    db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test, func_return_false, func_return_true

this_dir = dirname(abspath(__file__))
sample_files_dir = join(this_dir, '..', 'sample_files_for_tests')
path_to_tests_results = join(sample_files_dir, 'users', '4', 'tests_results')
working_dir = join(this_dir, 'working_dir_charts_creator')


class TestChartsCreator(TestCase):
    def cmp_accumulators(self, acc1: PValuesAccumulator, acc2: PValuesAccumulator):
        self.assertEqual(acc1.get_all_test_ids(), acc2.get_all_test_ids())
        for test_id in acc1.get_all_test_ids():
            dto1 = acc1.get_dto_for_test(test_id)
            dto2 = acc2.get_dto_for_test(test_id)
            self.assertEqual(dto1, dto2)

    def mock_func(self, func_name, side_effect):
        patcher = patch(func_name, side_effect=side_effect)
        self.addCleanup(patcher.stop)
        patcher.start()

    def mock(self):
        self.mock_func('managers.dbtestmanager.DBTestManager.get_test_by_id',
                       db_test_dao_get_test_by_id)
        self.mock_func('managers.dbtestmanager.DBTestManager.get_tests_by_id_list',
                       db_test_dao_get_tests_by_id_list)
        self.mock_func('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                       nist_dao_get_nist_param_for_test)
        self.mock_func('managers.resultsmanager.ResultsManager.get_paths_for_test_ids',
                       results_dao_get_paths_for_test_ids)

    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.mock()
        self.test1_id = TestsIdData.test1_id
        self.test2_id = TestsIdData.test2_id
        self.test3_id = TestsIdData.test3_id
        self.test4_id = TestsIdData.test4_id
        self.test5_id = TestsIdData.test5_id
        self.non_existing_test_id = TestsIdData.non_existing_test_id

        self.file1_id = FileIdData.file1_id
        self.file2_id = FileIdData.file2_id

        config_storage = MagicMock(nist='nist')
        self.charts_creator = ChartsCreator(None, config_storage)

        tests_arr = [self.test1_id, self.test2_id, self.test3_id, self.test4_id, self.test5_id]
        chart_dto = PValuesChartDto(0.01, 'tests', 'p-value', 'p-values chart')
        self.generate_charts_dto = GenerateChartsDto(tests_arr, {ChartType.P_VALUES: [chart_dto]}, working_dir)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_supported_charts(self):
        expected = [ChartType.P_VALUES, ChartType.P_VALUES_ZOOMED, ChartType.HISTOGRAM,
                    ChartType.TESTS_DEPENDENCY, ChartType.ECDF, ChartType.BOXPLOT_PT, ChartType.PROPORTIONS]
        self.assertEqual(expected, self.charts_creator.supported_charts)

    def test_reset(self):
        self.charts_creator._tests_with_dirs = ['something']
        self.charts_creator._p_values_accumulators[456] = ['asdf']
        self.charts_creator._loaded_items = True
        charts_storage_id = id(self.charts_creator._charts_storage)

        self.charts_creator.reset()

        self.assertIsNone(self.charts_creator._tests_with_dirs)
        self.assertEqual({}, self.charts_creator._p_values_accumulators)
        self.assertFalse(self.charts_creator._loaded_items)
        self.assertNotEqual(charts_storage_id, id(self.charts_creator._charts_storage))

    def test_load_p_values(self):
        test_ids = [self.test1_id, self.test2_id]
        expected = results_dao_get_paths_for_test_ids(test_ids)
        self.charts_creator.load_p_values(test_ids)
        self.assertEqual(expected, self.charts_creator._tests_with_dirs)

    def test_load_p_values_caching(self):
        test_ids = [self.test1_id, self.test2_id]
        self.charts_creator.load_p_values(test_ids)
        accumulators = self.charts_creator._p_values_accumulators
        self.charts_creator.load_p_values(test_ids)
        self.charts_creator.load_p_values(test_ids)
        self.charts_creator.load_p_values(test_ids)
        self.charts_creator.load_p_values(test_ids)

        self.assertEqual(1, self.charts_creator._results_dao.get_paths_for_test_ids.call_count)
        self.assertTrue(accumulators is self.charts_creator._p_values_accumulators)

    def test_accumulators_in_load_p_values(self):
        test_ids = [self.test1_id, self.test2_id, self.test3_id, self.test4_id, self.test5_id]

        acc1 = PValuesAccumulator()
        dto = PValuesDto(dict_for_test_13)
        acc1.add(self.test1_id, dto)
        dto = PValuesDto(dict_for_test_14)
        acc1.add(self.test2_id, dto)
        dto = PValuesDto(dict_for_test_41)
        acc1.add(self.test3_id, dto)

        acc2 = PValuesAccumulator()
        dto = PValuesDto(dict_for_test_42)
        acc2.add(self.test4_id, dto)
        dto = PValuesDto(dict_for_test_43)
        acc2.add(self.test5_id, dto)

        expected = {self.file1_id: acc1, self.file2_id: acc2}
        self.charts_creator.load_p_values(test_ids)

        self.cmp_accumulators(expected[self.file1_id], self.charts_creator._p_values_accumulators[self.file1_id])
        self.cmp_accumulators(expected[self.file2_id], self.charts_creator._p_values_accumulators[self.file2_id])

    def test_subset_from_tests(self):
        test_ids = [self.test1_id, self.test2_id, self.test3_id, self.test4_id, self.test5_id]
        self.charts_creator.load_p_values(test_ids)

        expected = []
        ret = self.charts_creator.get_subset_from_tests([])
        self.assertEqual(expected, ret)

        test_ids = [self.test1_id]
        expected = results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

        test_ids = [self.test1_id, self.test2_id]
        expected = results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

        test_ids = [self.test1_id, self.test2_id, self.test3_id]
        expected = results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

        test_ids = [self.test1_id, self.test2_id, self.test3_id, self.test4_id]
        expected = results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

        test_ids = [self.test1_id, self.test2_id, self.test3_id, self.test4_id, self.test5_id]
        expected = results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

    def test_generate_charts_none_dto(self):
        ret = self.charts_creator.generate_charts(None)
        self.assertIsNone(ret)

    def test_generate_charts_none_tests(self):
        self.generate_charts_dto.test_ids = None
        with self.assertRaises(TypeError) as context:
            self.charts_creator.generate_charts(self.generate_charts_dto)
        self.assertEqual('Test ids are None', str(context.exception))

    def test_generate_charts_empty_test_list(self):
        self.generate_charts_dto.test_ids = []
        with self.assertRaises(ValueError) as context:
            self.charts_creator.generate_charts(self.generate_charts_dto)
        self.assertEqual('No test ids specified', str(context.exception))

    def test_generate_charts_none_chart_types(self):
        self.generate_charts_dto.chart_types = None
        with self.assertRaises(TypeError) as context:
            self.charts_creator.generate_charts(self.generate_charts_dto)
        self.assertEqual('Chart types are None', str(context.exception))

    def test_generate_charts_empty_chart_types(self):
        self.generate_charts_dto.chart_types = {}
        with self.assertRaises(ValueError) as context:
            self.charts_creator.generate_charts(self.generate_charts_dto)
        self.assertEqual('No chart type specified', str(context.exception))

    def test_generate_charts_none_directory(self):
        self.generate_charts_dto.directory = None
        with self.assertRaises(TypeError) as context:
            self.charts_creator.generate_charts(self.generate_charts_dto)
        self.assertEqual('Directory is None', str(context.exception))

    def test_generate_charts_non_existing_dir(self):
        self.generate_charts_dto.directory = working_dir + '_something'
        with self.assertRaises(ValueError) as context:
            self.charts_creator.generate_charts(self.generate_charts_dto)
        self.assertEqual('Given directory: ' + self.generate_charts_dto.directory + ' does not exists',
                         str(context.exception))

    def test_generate_p_values_chart_for_tests_on_one_file(self):
        self.generate_charts_dto.test_ids = [self.test1_id, self.test2_id, self.test3_id]
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)
        file = join(working_dir, 'p_values_for_file_' + str(self.file1_id) + '.png')
        expected_chart_info = ChartInfo(None, file, ChartType.P_VALUES, self.file1_id)

        self.assertTrue(exists(file))
        self.assertEqual(1, len(storage.get_all_items()))
        self.assertEqual(expected_chart_info, storage.get_all_items()[0].ch_info)

    def test_generate_zoomed_p_values_chart(self):
        self.generate_charts_dto.test_ids = [self.test1_id, self.test2_id, self.test3_id]
        chart_dto = PValuesChartDto(0.01, 'tests', 'p-value', 'p-values chart', True)
        self.generate_charts_dto.chart_types[ChartType.P_VALUES_ZOOMED] = [chart_dto]
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        file1 = join(working_dir, 'p_values_for_file_' + str(self.file1_id) + '.png')
        chart_info1 = ChartInfo(None, file1, ChartType.P_VALUES, self.file1_id)

        file2 = join(working_dir, 'p_values_for_file_' + str(self.file1_id) + '_zoomed.png')
        chart_info2 = ChartInfo(None, file2, ChartType.P_VALUES_ZOOMED, self.file1_id)

        self.assertTrue(exists(file1))
        self.assertTrue(exists(file2))
        self.assertEqual(2, len(storage.get_all_items()))

        items = storage.get_all_items()

        info = list(filter(lambda cs_item: cs_item.ch_info.chart_type == ChartType.P_VALUES, items))[0].ch_info
        self.assertEqual(chart_info1, info)

        info = list(filter(lambda cs_item: cs_item.ch_info.chart_type == ChartType.P_VALUES_ZOOMED, items))[0].ch_info
        self.assertEqual(chart_info2, info)

    def test_create_p_values_chart_for_tests_two_files(self):
        file1 = join(working_dir, 'p_values_for_file_' + str(self.file1_id) + '.png')
        file2 = join(working_dir, 'p_values_for_file_' + str(self.file2_id) + '.png')

        expected_info_1 = ChartInfo(None, file1, ChartType.P_VALUES, self.file1_id)
        expected_info_2 = ChartInfo(None, file2, ChartType.P_VALUES, self.file2_id)
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        self.assertTrue(exists(file1))
        self.assertTrue(exists(file2))
        self.assertEqual(2, len(storage.get_all_items()))
        self.assertEqual(expected_info_1, storage.get_all_items()[0].ch_info)
        self.assertEqual(expected_info_2, storage.get_all_items()[1].ch_info)

    def test_create_histogram_for_two_files(self):
        file1 = join(working_dir, 'histogram_for_file_' + str(self.file1_id) + '.png')
        file2 = join(working_dir, 'histogram_for_file_' + str(self.file2_id) + '.png')

        expected_info_1 = ChartInfo(None, file1, ChartType.HISTOGRAM, self.file1_id)
        expected_info_2 = ChartInfo(None, file2, ChartType.HISTOGRAM, self.file2_id)

        histogram_dto = HistogramDto('intervals', 'number of p-values', 'histogram')
        self.generate_charts_dto.chart_types = {ChartType.HISTOGRAM: [histogram_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        self.assertTrue(exists(file1))
        self.assertTrue(exists(file2))
        self.assertEqual(2, len(storage.get_all_items()))
        self.assertEqual(expected_info_1, storage.get_all_items()[0].ch_info)
        self.assertEqual(expected_info_2, storage.get_all_items()[1].ch_info)

    @patch('common.unif_check.UnifCheck.check_for_uniformity', side_effect=func_return_true)
    @patch('common.unif_check.UnifCheck.get_p_value', return_value=0.5)
    @patch('common.unif_check.UnifCheck.is_approx_fulfilled', return_value=True)
    def test_create_tests_dependency_charts_for_one_file(self, func_check, func_get, func_is_approx):
        file = join(working_dir, 'dependency_of_Frequency_and_Cumulative_Sums_data_1.png')

        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(self.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(self.test2_id, PValuesFileType.DATA, 1))
        tests_dep_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_UNIFORM, seq_acc, 'Dependency of two tests')
        self.generate_charts_dto.test_ids = [self.test1_id, self.test2_id]
        self.generate_charts_dto.chart_types = {ChartType.TESTS_DEPENDENCY: [tests_dep_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        items = storage.get_all_items()
        info = items[0].ch_info
        self.assertEqual(1, len(items))
        self.assertEqual(file, info.path_to_chart)
        self.assertEqual(ChartType.TESTS_DEPENDENCY, info.chart_type)
        self.assertEqual(self.file1_id, info.file_id)

    @patch('common.unif_check.UnifCheck.check_for_uniformity', side_effect=func_return_true)
    @patch('common.unif_check.UnifCheck.get_p_value', return_value=0.5)
    @patch('common.unif_check.UnifCheck.is_approx_fulfilled', return_value=True)
    def test_create_tests_dependency_charts_more_sequences_than_test_ids(self, func_check, func_get, func_is_approx):
        file = join(working_dir, 'dependency_of_Frequency_and_Cumulative_Sums_data_1.png')

        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(self.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(self.test2_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(self.test3_id, PValuesFileType.DATA, 2))
        seq_acc.add_sequence(PValueSequence(self.test4_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(self.test5_id, PValuesFileType.RESULTS))

        tests_dep_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_UNIFORM, seq_acc, 'Dependency of two tests')
        self.generate_charts_dto.test_ids = [self.test1_id, self.test2_id]
        self.generate_charts_dto.chart_types = {ChartType.TESTS_DEPENDENCY: [tests_dep_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        items = storage.get_all_items()
        info = items[0].ch_info
        self.assertEqual(1, len(items))
        self.assertEqual(file, info.path_to_chart)
        self.assertEqual(ChartType.TESTS_DEPENDENCY, info.chart_type)
        self.assertEqual(self.file1_id, info.file_id)

    @patch('common.unif_check.UnifCheck.check_for_uniformity', side_effect=func_return_true)
    @patch('common.unif_check.UnifCheck.get_p_value', return_value=0.5)
    @patch('common.unif_check.UnifCheck.is_approx_fulfilled', return_value=True)
    def test_create_three_tests_dependency_charts_for_one_file(self, func_check, func_get, func_is_approx):
        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(self.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(self.test2_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(self.test3_id, PValuesFileType.DATA, 2))

        tests_dep_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_UNIFORM, seq_acc, 'Dependency of two tests')
        self.generate_charts_dto.test_ids = [self.test1_id, self.test2_id, self.test3_id]
        self.generate_charts_dto.chart_types = {ChartType.TESTS_DEPENDENCY: [tests_dep_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        items = storage.get_all_items()
        self.assertEqual(3, len(items))

        info = items[0].ch_info
        file = join(working_dir, 'dependency_of_Frequency_and_Cumulative_Sums_data_1.png')
        self.assertEqual(file, info.path_to_chart)
        self.assertEqual(ChartType.TESTS_DEPENDENCY, info.chart_type)
        self.assertEqual(self.file1_id, info.file_id)

        info = items[1].ch_info
        file = join(working_dir, 'dependency_of_Frequency_and_Serial_data_2.png')
        self.assertEqual(file, info.path_to_chart)
        self.assertEqual(ChartType.TESTS_DEPENDENCY, info.chart_type)
        self.assertEqual(self.file1_id, info.file_id)

        info = items[2].ch_info
        file = join(working_dir, 'dependency_of_Cumulative_Sums_data_1_and_Serial_data_2.png')
        self.assertEqual(file, info.path_to_chart)
        self.assertEqual(ChartType.TESTS_DEPENDENCY, info.chart_type)
        self.assertEqual(self.file1_id, info.file_id)

    @patch('common.unif_check.UnifCheck.check_for_uniformity', side_effect=func_return_true)
    @patch('common.unif_check.UnifCheck.get_p_value', return_value=0.5)
    @patch('common.unif_check.UnifCheck.is_approx_fulfilled', return_value=True)
    def test_create_tests_dependency_charts_for_two_files(self, func_check, func_get, func_is_approx):
        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(self.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(self.test2_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(self.test4_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(self.test5_id, PValuesFileType.RESULTS))

        tests_dep_dto = TestDependencyDto(0.01, FilterUniformity.REMOVE_UNIFORM, seq_acc, 'Dependency of two tests')
        self.generate_charts_dto.test_ids = [self.test1_id, self.test2_id, self.test4_id, self.test5_id]
        self.generate_charts_dto.chart_types = {ChartType.TESTS_DEPENDENCY: [tests_dep_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        items = storage.get_all_items()
        self.assertEqual(2, len(items))

        info = items[0].ch_info
        file = join(working_dir, 'dependency_of_Frequency_and_Cumulative_Sums_data_1.png')
        self.assertEqual(file, info.path_to_chart)
        self.assertEqual(ChartType.TESTS_DEPENDENCY, info.chart_type)
        self.assertEqual(self.file1_id, info.file_id)

        info = items[1].ch_info
        file = join(working_dir, 'dependency_of_Linear_Complexity_and_Longest_Run_of_Ones.png')
        self.assertEqual(file, info.path_to_chart)
        self.assertEqual(ChartType.TESTS_DEPENDENCY, info.chart_type)
        self.assertEqual(self.file2_id, info.file_id)

    def test_create_ecdf_for_one_file(self):
        file1 = join(working_dir, 'ecdf_for_test_{}_results.png'.format(self.test1_id))
        file2 = join(working_dir, 'ecdf_for_test_{}_data_1.png'.format(self.test2_id))

        seq1 = PValueSequence(self.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(self.test2_id, PValuesFileType.DATA, 1)
        ds_info1 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq1)
        ds_info2 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq2)
        expected_info_1 = ChartInfo(ds_info1, file1, ChartType.ECDF, self.file1_id)
        expected_info_2 = ChartInfo(ds_info2, file2, ChartType.ECDF, self.file1_id)

        ecdf_dto = EcdfDto(0.05, 'ECDF', 'p-value', 'Cumulative density', 'Empirical', 'Theoretical', [seq1, seq2])
        self.generate_charts_dto.chart_types = {ChartType.ECDF: [ecdf_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        self.assertTrue(exists(file1))
        self.assertTrue(exists(file2))
        self.assertEqual(2, len(storage.get_all_items()))
        self.assertEqual(expected_info_1, storage.get_all_items()[0].ch_info)
        self.assertEqual(expected_info_2, storage.get_all_items()[1].ch_info)

    def test_create_ecdf_for_five_files(self):
        file1 = join(working_dir, 'ecdf_for_test_{}_results.png'.format(self.test1_id))
        file2 = join(working_dir, 'ecdf_for_test_{}_data_1.png'.format(self.test2_id))
        file3 = join(working_dir, 'ecdf_for_test_{}_data_2.png'.format(self.test3_id))
        file4 = join(working_dir, 'ecdf_for_test_{}_results.png'.format(self.test4_id))
        file5 = join(working_dir, 'ecdf_for_test_{}_results.png'.format(self.test5_id))

        seq1 = PValueSequence(self.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(self.test2_id, PValuesFileType.DATA, 1)
        seq3 = PValueSequence(self.test3_id, PValuesFileType.DATA, 2)
        seq4 = PValueSequence(self.test4_id, PValuesFileType.RESULTS)
        seq5 = PValueSequence(self.test5_id, PValuesFileType.RESULTS)

        ds_info1 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq1)
        ds_info2 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq2)
        ds_info3 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq3)
        ds_info4 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq4)
        ds_info5 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq5)

        expected_info_1 = ChartInfo(ds_info1, file1, ChartType.ECDF, self.file1_id)
        expected_info_2 = ChartInfo(ds_info2, file2, ChartType.ECDF, self.file1_id)
        expected_info_3 = ChartInfo(ds_info3, file3, ChartType.ECDF, self.file1_id)
        expected_info_4 = ChartInfo(ds_info4, file4, ChartType.ECDF, self.file2_id)
        expected_info_5 = ChartInfo(ds_info5, file5, ChartType.ECDF, self.file2_id)

        ecdf_dto = EcdfDto(0.05, 'ECDF', 'p-value', 'Cumulative density', 'Empirical', 'Theoretical',
                           [seq1, seq2, seq3, seq4, seq5])
        self.generate_charts_dto.chart_types = {ChartType.ECDF: [ecdf_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        self.assertTrue(exists(file1))
        self.assertTrue(exists(file2))
        self.assertEqual(5, len(storage.get_all_items()))
        self.assertEqual(expected_info_1, storage.get_all_items()[0].ch_info)
        self.assertEqual(expected_info_2, storage.get_all_items()[1].ch_info)
        self.assertEqual(expected_info_3, storage.get_all_items()[2].ch_info)
        self.assertEqual(expected_info_4, storage.get_all_items()[3].ch_info)
        self.assertEqual(expected_info_5, storage.get_all_items()[4].ch_info)

    def test_generate_boxplots_one_file(self):
        file = join(working_dir, 'boxplot_pt_{}.png'.format(self.test1_id))

        seq1 = PValueSequence(self.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(self.test2_id, PValuesFileType.DATA, 1)

        seqcs = [[seq1, seq2]]
        boxplot_dto = BoxplotPTDto('Boxplot(s) per tests', seqcs)
        self.generate_charts_dto.chart_types = {ChartType.BOXPLOT_PT: [boxplot_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)
        self.assertTrue(exists(file))
        self.assertEqual(1, len(storage.get_all_items()))

        ch_info = storage.get_all_items()[0].ch_info
        expected = ChartInfo(DataSourceInfo(TestsInChart.MULTIPLE_TESTS, seqcs[0]), file, ChartType.BOXPLOT_PT,
                             FileIdData.file1_id)
        self.assertEqual(expected, ch_info)

    def test_generate_boxplots_three_files(self):
        file1 = join(working_dir, 'boxplot_pt_{}.png'.format(TestsIdData.test1_id))
        file2 = join(working_dir, 'boxplot_pt_{}.png'.format(TestsIdData.test2_id))
        file3 = join(working_dir, 'boxplot_pt_{}.png'.format(TestsIdData.test4_id))

        seq1 = PValueSequence(self.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(self.test2_id, PValuesFileType.DATA, 1)
        seq3 = PValueSequence(self.test2_id, PValuesFileType.DATA, 2)
        seq4 = PValueSequence(self.test3_id, PValuesFileType.DATA, 1)
        seq5 = PValueSequence(self.test4_id, PValuesFileType.RESULTS)
        seq6 = PValueSequence(self.test5_id, PValuesFileType.RESULTS)

        seqcs = [[seq1], [seq2, seq3, seq4], [seq5, seq6]]
        boxplot_dto = BoxplotPTDto('Boxplot(s) per tests', seqcs)
        self.generate_charts_dto.chart_types = {ChartType.BOXPLOT_PT: [boxplot_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)
        self.assertTrue(exists(file1))
        self.assertTrue(exists(file2))
        self.assertTrue(exists(file3))
        self.assertEqual(3, len(storage.get_all_items()))

        ch_info = storage.get_all_items()[0].ch_info
        expected = ChartInfo(DataSourceInfo(TestsInChart.MULTIPLE_TESTS, seqcs[0]), file1, ChartType.BOXPLOT_PT,
                             FileIdData.file1_id)
        self.assertEqual(expected, ch_info)

        ch_info = storage.get_all_items()[1].ch_info
        expected = ChartInfo(DataSourceInfo(TestsInChart.MULTIPLE_TESTS, seqcs[1]), file2, ChartType.BOXPLOT_PT,
                             FileIdData.file1_id)
        self.assertEqual(expected, ch_info)

        ch_info = storage.get_all_items()[2].ch_info
        expected = ChartInfo(DataSourceInfo(TestsInChart.MULTIPLE_TESTS, seqcs[2]), file3, ChartType.BOXPLOT_PT,
                             FileIdData.file2_id)
        self.assertEqual(expected, ch_info)

    def test_generate_proportions_chart(self):
        dto = ProportionsDto(0.01, 'Proportions of passing sequences', 'tests', 'proportion', PropFormula.ORIGINAL,
                             short_names_dict)
        self.generate_charts_dto.chart_types = {ChartType.PROPORTIONS: [dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)
        items = storage.get_all_items()
        self.assertEqual(2, len(items))
        item = items[0]  # type: ChartsStorageItem
        file_name = join(working_dir, 'prop_first_test_id_{}.png'.format(TestsIdData.test1_id))
        expected_ch_info = ChartInfo(None, file_name, ChartType.PROPORTIONS, FileIdData.file1_id)
        self.assertEqual(expected_ch_info, item.ch_info)
        self.assertIsNone(item.info)
        self.assertIsNone(item.err)
        self.assertTrue(exists(file_name))

        item = items[1]  # type: ChartsStorageItem
        file_name = join(working_dir, 'prop_first_test_id_{}.png'.format(TestsIdData.test4_id))
        expected_ch_info = ChartInfo(None, file_name, ChartType.PROPORTIONS, FileIdData.file2_id)
        self.assertEqual(expected_ch_info, item.ch_info)
        self.assertIsNone(item.info)
        self.assertIsNone(item.err)
        self.assertTrue(exists(file_name))

        infos = storage.get_infos_for_chart_type(ChartType.PROPORTIONS)
        self.assertEqual([], infos)
        errs = storage.get_errors_for_chart_type(ChartType.PROPORTIONS)
        self.assertEqual([], errs)

    @patch('charts.proportions.proportions_extractor.ProportionsExtractor.get_proportions',
           side_effect=DifferentNumOfPValsError('message', 456, 400))
    def test_generate_prop_charts_err_propagation(self, f_get_proportions):
        dto = ProportionsDto(0.01, 'Proportions of passing sequences', 'tests', 'proportion', PropFormula.ORIGINAL)
        self.generate_charts_dto.chart_types = {ChartType.PROPORTIONS: [dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        self.assertEqual([], storage.get_all_items())

        infos = storage.get_infos_for_chart_type(ChartType.PROPORTIONS)
        self.assertEqual([], infos)

        errs = storage.get_errors_for_chart_type(ChartType.PROPORTIONS)
        self.assertEqual(1, len(errs))
        expected = PropDiffLenErr(456, 400)
        self.assertEqual(expected, errs[0])


    def test_draw_concrete_charts_for_non_existing_chart_type(self):
        chart_dto = PValuesChartDto(0.01, 'tests', 'p-value', 'p-values chart')
        with self.assertRaises(ChartsError) as context:
            self.charts_creator.draw_concrete_charts(-1, chart_dto, working_dir)
        self.assertEqual('Unsupported chart type', str(context.exception))
