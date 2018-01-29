from os import makedirs
from os.path import dirname, abspath, join, exists
from shutil import rmtree
from unittest import TestCase
from unittest.mock import MagicMock

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_creator import ChartsCreator
from charts.generate_charts_dto import GenerateChartsDto
from charts.histogram_dto import HistogramDto
from charts.p_values_chart_dto import PValuesChartDto
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, dict_for_test_41, dict_for_test_42, \
    dict_for_test_43
from tests.data_for_tests.common_functions import results_dao_get_paths_for_test_ids, db_test_dao_get_tests_by_id_list, \
    db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test

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

    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.test1_id = 13
        self.test2_id = 14
        self.test3_id = 41
        self.test4_id = 42
        self.test5_id = 43
        self.non_existing_test_id = 123456

        self.file1_id = 456
        self.file2_id = 786

        config_storage = MagicMock()
        config_storage.nist = 'nist'
        self.charts_creator = ChartsCreator(None, config_storage)
        self.charts_creator._results_dao.get_paths_for_test_ids = MagicMock(side_effect=
                                                                            results_dao_get_paths_for_test_ids)
        self.charts_creator._tests_dao.get_tests_by_id_list = MagicMock(side_effect=
                                                                        db_test_dao_get_tests_by_id_list)
        self.charts_creator._p_values_creator._extractor._test_dao.get_test_by_id = \
            MagicMock(side_effect=db_test_dao_get_test_by_id)
        self.charts_creator._p_values_creator._extractor._nist_dao.get_nist_param_for_test = \
            MagicMock(side_effect=nist_dao_get_nist_param_for_test)
        tests_arr = [self.test1_id, self.test2_id, self.test3_id, self.test4_id, self.test5_id]
        chart_dto = PValuesChartDto(0.01, 'tests', 'p-value', 'p-values chart')
        self.generate_charts_dto = GenerateChartsDto(tests_arr, {ChartType.P_VALUES: [chart_dto]}, working_dir)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

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
        with self.assertRaises(TypeError) as context:
            self.charts_creator.generate_charts(None)
        self.assertEqual('Charts DTO is None', str(context.exception))

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
        expected_chart_info = ChartInfo(file, ChartType.P_VALUES, self.file1_id)

        self.assertTrue(exists(file))
        self.assertEqual(1, len(storage.get_all_infos()))
        self.assertEqual(expected_chart_info, storage.get_all_infos()[0])

    def test_create_p_values_chart_for_tests_two_files(self):
        file1 = join(working_dir, 'p_values_for_file_' + str(self.file1_id) + '.png')
        file2 = join(working_dir, 'p_values_for_file_' + str(self.file2_id) + '.png')

        expected_info_1 = ChartInfo(file1, ChartType.P_VALUES, self.file1_id)
        expected_info_2 = ChartInfo(file2, ChartType.P_VALUES, self.file2_id)
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        self.assertTrue(exists(file1))
        self.assertTrue(exists(file2))
        self.assertEqual(2, len(storage.get_all_infos()))
        self.assertEqual(expected_info_1, storage.get_all_infos()[0])
        self.assertEqual(expected_info_2, storage.get_all_infos()[1])

    def test_create_histogram_for_two_files(self):
        file1 = join(working_dir, 'histogram_for_file_' + str(self.file1_id) + '.png')
        file2 = join(working_dir, 'histogram_for_file_' + str(self.file2_id) + '.png')

        expected_info_1 = ChartInfo(file1, ChartType.HISTOGRAM, self.file1_id)
        expected_info_2 = ChartInfo(file2, ChartType.HISTOGRAM, self.file2_id)

        histogram_dto = HistogramDto('intervals', 'number of p-values', 'histogram')
        self.generate_charts_dto.chart_types = {ChartType.HISTOGRAM: [histogram_dto]}
        storage = self.charts_creator.generate_charts(self.generate_charts_dto)

        self.assertTrue(exists(file1))
        self.assertTrue(exists(file2))
        self.assertEqual(2, len(storage.get_all_infos()))
        self.assertEqual(expected_info_1, storage.get_all_infos()[0])
        self.assertEqual(expected_info_2, storage.get_all_infos()[1])
