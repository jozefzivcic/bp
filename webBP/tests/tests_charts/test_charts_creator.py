from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase
from unittest.mock import MagicMock

from shutil import rmtree

from charts.chart_options import ChartOptions
from charts.charts_creator import ChartsCreator
from charts.charts_error import ChartsError
from models.nistparam import NistParam
from models.test import Test
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, dict_for_test_41, dict_for_test_42, \
    dict_for_test_43

this_dir = dirname(abspath(__file__))
sample_files_dir = join(this_dir, '..', 'sample_files_for_tests')
path_to_tests_results = join(sample_files_dir, 'users', '4', 'tests_results')
working_dir = join(this_dir, 'working_dir')


class TestChartsCreator(TestCase):
    def results_dao_get_paths_for_test_ids(self, test_ids: list) -> list:
        ret = []
        if self.test1_id in test_ids:
            ret.append((self.test1_id, join(path_to_tests_results, str(self.test1_id))))
        if self.test2_id in test_ids:
            ret.append((self.test2_id, join(path_to_tests_results, str(self.test2_id))))
        if self.test3_id in test_ids:
            ret.append((self.test3_id, join(path_to_tests_results, str(self.test3_id))))
        if self.test4_id in test_ids:
            ret.append((self.test4_id, join(path_to_tests_results, str(self.test4_id))))
        if self.test5_id in test_ids:
            ret.append((self.test5_id, join(path_to_tests_results, str(self.test5_id))))
        return ret

    def db_test_dao_get_tests_by_id_list(self, test_ids: list) -> list:
        ret = []
        if self.test1_id in test_ids:
            ret.append(self.db_test_dao_get_test_by_id(self.test1_id))
        if self.test2_id in test_ids:
            ret.append(self.db_test_dao_get_test_by_id(self.test2_id))
        if self.test3_id in test_ids:
            ret.append(self.db_test_dao_get_test_by_id(self.test3_id))
        if self.test4_id in test_ids:
            ret.append(self.db_test_dao_get_test_by_id(self.test4_id))
        if self.test5_id in test_ids:
            ret.append(self.db_test_dao_get_test_by_id(self.test5_id))
        return ret

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
        if self.test4_id == test_id:
            test.id = self.test4_id
            test.file_id = self.file2_id
            return test
        if self.test5_id == test_id:
            test.id = self.test5_id
            test.file_id = self.file2_id
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
        if self.test4_id == test.id:
            param.test_number = 15
            return param
        if self.test5_id == test.id:
            param.test_number = 5
            return param
        return None

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

        chart_options = ChartOptions()
        chart_options.x_label = 'tests'
        chart_options.y_label = 'p-value'
        chart_options.title = 'p-values chart'
        config_storage = MagicMock()
        config_storage.nist = 'nist'
        self.charts_creator = ChartsCreator(chart_options, None, config_storage)
        self.charts_creator._results_dao.get_paths_for_test_ids = MagicMock(side_effect=
                                                                            self.results_dao_get_paths_for_test_ids)
        self.charts_creator._tests_dao.get_tests_by_id_list = MagicMock(side_effect=
                                                                        self.db_test_dao_get_tests_by_id_list)
        self.charts_creator._extractor._test_dao.get_test_by_id = MagicMock(side_effect=self.db_test_dao_get_test_by_id)
        self.charts_creator._extractor._nist_dao.get_nist_param_for_test = \
            MagicMock(side_effect=self.nist_dao_get_nist_param_for_test)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_reset(self):
        self.charts_creator._tests_with_dirs = ['something']
        self.charts_creator._p_values_accumulators[456] = ['asdf']
        self.charts_creator._loaded_items = True
        self.charts_creator.reset()
        self.assertIsNone(self.charts_creator._tests_with_dirs)
        self.assertEqual({}, self.charts_creator._p_values_accumulators)
        self.assertFalse(self.charts_creator._loaded_items)

    def test_load_p_values(self):
        test_ids = [self.test1_id, self.test2_id]
        expected = self.results_dao_get_paths_for_test_ids(test_ids)
        self.charts_creator.load_p_values(test_ids)
        self.assertEqual(expected, self.charts_creator._tests_with_dirs)

    def test_load_p_values_caching(self):
        test_ids = [self.test1_id, self.test2_id]
        self.charts_creator.load_p_values(test_ids)
        accumulator = self.charts_creator._p_values_accumulators
        self.charts_creator.load_p_values(test_ids)
        self.charts_creator.load_p_values(test_ids)
        self.charts_creator.load_p_values(test_ids)
        self.charts_creator.load_p_values(test_ids)

        self.assertEqual(1, self.charts_creator._results_dao.get_paths_for_test_ids.call_count)
        self.assertTrue(accumulator is self.charts_creator._p_values_accumulators)

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
        expected = self.results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

        test_ids = [self.test1_id, self.test2_id]
        expected = self.results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

        test_ids = [self.test1_id, self.test2_id, self.test3_id]
        expected = self.results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

        test_ids = [self.test1_id, self.test2_id, self.test3_id, self.test4_id]
        expected = self.results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

        test_ids = [self.test1_id, self.test2_id, self.test3_id, self.test4_id, self.test5_id]
        expected = self.results_dao_get_paths_for_test_ids(test_ids)
        ret = self.charts_creator.get_subset_from_tests(test_ids)
        self.assertEqual(expected, ret)

    def test_create_one_p_values_chart_throws_error_on_accumulator(self):
        with self.assertRaises(TypeError) as context:
            self.charts_creator.create_one_p_values_chart_for_tests(None, 'something')
            self.assertEqual('Accumulator cannot be None' in str(context.exception))

    def test_create_one_p_values_chart_throws_error_on_file_none(self):
        with self.assertRaises(TypeError) as context:
            self.charts_creator.create_one_p_values_chart_for_tests(PValuesAccumulator(), None)
            self.assertEqual('File cannot be None' in str(context.exception))

    def test_create_one_p_values_chart(self):
        acc = PValuesAccumulator()
        dto = PValuesDto(dict_for_test_13)
        acc.add(self.test1_id, dto)
        dto = PValuesDto(dict_for_test_14)
        acc.add(self.test2_id, dto)
        dto = PValuesDto(dict_for_test_41)
        acc.add(self.test3_id, dto)

        file_name = join(working_dir, 'graph.png')
        self.charts_creator.create_one_p_values_chart_for_tests(acc, file_name)
        self.assertTrue(exists(file_name))

    def test_create_p_values_charts_for_tests_none_tests(self):
        with self.assertRaises(TypeError) as context:
            self.charts_creator.create_p_values_charts_for_tests(None, working_dir)
            self.assertEqual('Test ids are None' in str(context.exception))

    def test_create_p_values_charts_for_tests_empty_test_list(self):
        with self.assertRaises(ValueError) as context:
            self.charts_creator.create_p_values_charts_for_tests([], working_dir)
            self.assertEqual('No test ids specified' in str(context.exception))

    def test_create_p_values_charts_for_tests_none_directory(self):
        test_ids = [self.test1_id, self.test2_id]
        with self.assertRaises(TypeError) as context:
            self.charts_creator.create_p_values_charts_for_tests(test_ids, None)
            self.assertEqual('No test ids specified' in str(context.exception))

    def test_create_p_values_charts_for_tests_non_existing_dir(self):
        test_ids = [self.test1_id, self.test2_id]
        non_existing_dir = working_dir + '_something'
        with self.assertRaises(ValueError) as context:
            self.charts_creator.create_p_values_charts_for_tests(test_ids, non_existing_dir)
            self.assertEqual('Given directory: ' + non_existing_dir + ' does not exists' in str(context.exception))

    def test_create_p_values_chart_for_tests_one_file(self):
        expected_file = join(working_dir, 'p_values_for_file_' + str(self.file1_id) + '.png')

        test_ids = [self.test1_id, self.test2_id, self.test3_id]
        self.charts_creator.create_p_values_charts_for_tests(test_ids, working_dir)

        self.assertTrue(exists(expected_file))

    def test_create_p_values_chart_for_tests_two_files(self):
        expected_file1 = join(working_dir, 'p_values_for_file_' + str(self.file1_id) + '.png')
        expected_file2 = join(working_dir, 'p_values_for_file_' + str(self.file2_id) + '.png')

        test_ids = [self.test1_id, self.test2_id, self.test3_id, self.test4_id, self.test5_id]
        self.charts_creator.create_p_values_charts_for_tests(test_ids, working_dir)

        self.assertTrue(exists(expected_file1))
        self.assertTrue(exists(expected_file2))

    def test_create_p_values_chart_for_tests_return_value(self):
        expected_file1 = join(working_dir, 'p_values_for_file_' + str(self.file1_id) + '.png')
        expected_file2 = join(working_dir, 'p_values_for_file_' + str(self.file2_id) + '.png')

        test_ids = [self.test1_id, self.test2_id, self.test3_id, self.test4_id, self.test5_id]
        storage = self.charts_creator.create_p_values_charts_for_tests(test_ids, working_dir)

        self.assertEqual(2, len(storage.get_all_paths()))
        self.assertTrue(expected_file1 in storage.get_all_paths())
        self.assertTrue(expected_file2 in storage.get_all_paths())
