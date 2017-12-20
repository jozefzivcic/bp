from os.path import dirname, abspath, join
from unittest import TestCase
from unittest.mock import MagicMock

from charts.charts_creator import ChartsCreator
from models.test import Test

this_dir = dirname(abspath(__file__))
sample_files_dir = join(this_dir, '..', 'sample_files_for_tests')
path_to_tests_results = join(sample_files_dir, 'users', '4', 'tests_results')


class TestChartsCreator(TestCase):
    def results_dao_side_effect(self, test_ids: list) -> list:
        ret = []
        if self.test1_id in test_ids:
            ret.append((self.test1_id, join(path_to_tests_results, str(self.test1_id))))
        elif self.test2_id in test_ids:
            ret.append((self.test2_id, join(path_to_tests_results, str(self.test2_id))))
        return ret

    def db_test_dao_side_effect(self, test_ids: list) -> list:
        ret = []
        if self.test1_id in test_ids:
            test = Test()
            test.id = self.test1_id
            test.file_id = self.file1_id
            ret.append(test)
        if self.test2_id in test_ids:
            test = Test()
            test.id = self.test2_id
            test.file_id = self.file1_id
            ret.append(test)
        return ret

    def setUp(self):
        self.test1_id = 13
        self.test2_id = 14
        self.file1_id = 456
        self.charts_creator = ChartsCreator(None, None, None)
        self.charts_creator._results_dao.get_paths_for_test_ids = MagicMock(side_effect=self.results_dao_side_effect)
        self.charts_creator._tests_dao.get_tests_by_id_list = MagicMock(side_effect=self.db_test_dao_side_effect)

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
        expected = self.results_dao_side_effect(test_ids)
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
