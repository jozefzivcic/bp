from unittest import TestCase

from os.path import join, dirname, abspath

from p_value_processing.nist_loader import NistLoader
from tests.tests_p_value_processing.common_data import dict_for_test_14, dict_for_test_13

this_dir = dirname(abspath(__file__))
sample_files_dir = join(this_dir, '..', 'sample_files_for_tests')


class TestNistLoader(TestCase):
    def setUp(self):
        self._nist_loader = NistLoader()

    def test_get_file_name_for_file_without_extension(self):
        sample_file = '/home/sth/Documents/file'
        expected_file = 'file'
        ret = self._nist_loader.get_file_name(sample_file)
        self.assertEqual(expected_file, ret)

    def test_get_file_name_for_file_with_extension(self):
        sample_file = '/home/sth/Documents/file.txt'
        expected_file = 'file'
        ret = self._nist_loader.get_file_name(sample_file)
        self.assertEqual(expected_file, ret)

    def test_loading_p_values_one_file(self):
        directory = join(sample_files_dir, 'users', '4', 'tests_results', '13')
        self._nist_loader.load_p_values_in_dir(directory)
        dict_in_loader = self._nist_loader._p_values_in_files
        self.assertEqual(dict_for_test_13, dict_in_loader)

    def test_loading_p_values_three_files(self):
        directory = join(sample_files_dir, 'users', '4', 'tests_results', '14')
        self._nist_loader.load_p_values_in_dir(directory)
        dict_in_loader = self._nist_loader._p_values_in_files
        self.assertEqual(dict_for_test_14, dict_in_loader)

    def test_generate_dto(self):
        directory = join(sample_files_dir, 'users', '4', 'tests_results', '13')
        self._nist_loader.load_p_values_in_dir(directory)
        dto = self._nist_loader.generate_dto()
        self.assertEqual(dict_for_test_13, dto._p_values_dict)

