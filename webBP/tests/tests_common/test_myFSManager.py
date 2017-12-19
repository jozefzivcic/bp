from os.path import abspath, dirname, join
from unittest import TestCase

from common.my_fs_manager import MyFSManager


class TestMyFSManager(TestCase):
    def setUp(self):
        self.fs_mgr = MyFSManager()
        this_dir = dirname(abspath(__file__))
        self.sample_files_dir = join(this_dir, '..', 'sample_files_for_tests')

    def test_get_data_files_one_file(self):
        relative_path = 'users/4/tests_results/12'
        test_dir = join(self.sample_files_dir, relative_path)
        dir_arr = self.fs_mgr.get_data_files_in_dir(test_dir)
        self.assertEqual(len(dir_arr), 1, 'Method did not return only one file')
        self.assertEqual(dir_arr[0], join(self.sample_files_dir, relative_path, 'results.txt'), 'Returned file is not '
                                                                                                'results.txt')

    def test_get_data_files_more_files(self):
        relative_path = 'users/4/tests_results/11'
        test_dir = join(self.sample_files_dir, relative_path)
        dir_arr = self.fs_mgr.get_data_files_in_dir(test_dir)
        self.assertEqual(len(dir_arr), 148, 'Method did not return 148 files')
        for i in range(0, 148):
            self.assertEqual(dir_arr[i], join(self.sample_files_dir, relative_path, 'data' + str(i + 1) + '.txt'),
                             'File on index ' + str(i) + ' is ' + dir_arr[i] + ' not ' +
                             join(self.sample_files_dir, relative_path, 'data' + str(i + 1) + '.txt'))

    def test_get_results_file_in_none_dir(self):
        ret = self.fs_mgr.get_results_file_in_dir(None)
        self.assertIsNone(ret)

    def test_get_results_file_in_dir(self):
        relative_path = 'users/4/tests_results/11'
        test_dir = join(self.sample_files_dir, relative_path)
        results_file = self.fs_mgr.get_results_file_in_dir(test_dir)
        self.assertEqual(join(test_dir, 'results.txt'), results_file, 'Returned file is not results.txt')

    def test_get_files_with_p_values_in_dir_no_file(self):
        relative_path = 'users/4/tests_results'
        test_dir = join(self.sample_files_dir, relative_path)
        ret = self.fs_mgr.get_files_with_p_values_in_dir(test_dir)
        expected_files = []
        self.assertEqual(expected_files, ret)

    def test_get_files_with_p_values_in_dir_one_file(self):
        relative_path = 'users/4/tests_results/12'
        test_dir = join(self.sample_files_dir, relative_path)
        ret = self.fs_mgr.get_files_with_p_values_in_dir(test_dir)
        expected_files = [join(test_dir, 'results.txt')]
        self.assertEqual(expected_files, ret)

    def test_get_files_with_p_values_in_dir_three_files(self):
        relative_path = 'users/4/tests_results/14'
        test_dir = join(self.sample_files_dir, relative_path)
        ret = self.fs_mgr.get_files_with_p_values_in_dir(test_dir)
        expected_files = [
            join(test_dir, 'data1.txt'),
            join(test_dir, 'data2.txt'),
            join(test_dir, 'results.txt')
        ]
        self.assertEqual(expected_files, ret)

    def test_get_files_with_p_values_in_dir_more_files(self):
        relative_path = 'users/4/tests_results/11'
        test_dir = join(self.sample_files_dir, relative_path)
        ret = self.fs_mgr.get_files_with_p_values_in_dir(test_dir)

        expected_files = []
        num_of_data_files = 148
        for i in range(1, num_of_data_files + 1):
            data_filename = 'data' + str(i) + '.txt'
            data_abs_path = join(test_dir, data_filename)
            expected_files.append(data_abs_path)
        expected_files.append(join(test_dir, 'results.txt'))
        self.assertEqual(expected_files, ret)
