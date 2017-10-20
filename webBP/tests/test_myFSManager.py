from os.path import abspath, dirname, join
from unittest import TestCase

from nist_statistics.my_fs_manager import MyFSManager


class TestMyFSManager(TestCase):
    def setUp(self):
        self.fs_mgr = MyFSManager()
        self.this_dir = dirname(abspath(__file__))

    def test_get_data_files_one_file(self):
        relative_path = 'users/4/tests_results/12'
        test_dir = join(self.this_dir, relative_path)
        dir_arr = self.fs_mgr.get_data_files_in_dir(test_dir)
        self.assertEqual(len(dir_arr), 1, 'Method did not return only one file')
        self.assertEqual(dir_arr[0], join(self.this_dir, relative_path, 'results.txt'), 'Returned file is not '
                                                                                        'results.txt')

    def test_get_data_files_more_files(self):
        relative_path = 'users/4/tests_results/11'
        test_dir = join(self.this_dir, relative_path)
        dir_arr = self.fs_mgr.get_data_files_in_dir(test_dir)
        self.assertEqual(len(dir_arr), 148, 'Method did not return 148 files')
        for i in range(0, 148):
            self.assertEqual(dir_arr[i], join(self.this_dir, relative_path, 'data' + str(i + 1) + '.txt'),
                             'File on index ' + str(i) + ' is ' + dir_arr[i] + ' not ' +
                             join(self.this_dir, relative_path, 'data' + str(i + 1) + '.txt'))

    def test_get_results_file_in_dir(self):
        relative_path = 'users/4/tests_results/11'
        test_dir = join(self.this_dir, relative_path)
        results_file = self.fs_mgr.get_results_file_in_dir(test_dir)
        self.assertEqual(join(test_dir, 'results.txt'), results_file, 'Returned file is not results.txt')
