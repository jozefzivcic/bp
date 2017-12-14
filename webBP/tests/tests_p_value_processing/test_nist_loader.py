from unittest import TestCase

from os.path import join, dirname, abspath

from p_value_processing.nist_loader import NistLoader

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
        expected_dict = {'results': [0.857153, 0.298340, 0.674485, 0.078408, 0.200545, 0.888660, 0.471525, 0.920344,
                                     0.357573, 0.509254]}
        self._nist_loader.load_p_values_in_dir(directory)
        dict_in_loader = self._nist_loader._p_values_in_files
        self.assertEqual(expected_dict, dict_in_loader)

    def test_loading_p_values_three_files(self):
        directory = join(sample_files_dir, 'users', '4', 'tests_results', '14')
        expected_dict = {'results': [0.593063, 0.759852, 0.584171, 0.483106, 0.849583, 0.475200, 0.131536, 0.131536,
                                     0.206201, 0.252025, 0.911652, 0.796727, 0.882140, 0.467379, 0.814758, 0.897326,
                                     0.160236, 0.483106, 0.684836, 0.532261],
                         'data1': [0.593063, 0.584171, 0.849583, 0.131536, 0.206201, 0.911652, 0.882140, 0.814758,
                                   0.160236, 0.684836],
                         'data2': [0.759852, 0.483106, 0.475200, 0.131536, 0.252025, 0.796727, 0.467379, 0.897326,
                                   0.483106, 0.532261]}
        self._nist_loader.load_p_values_in_dir(directory)
        dict_in_loader = self._nist_loader._p_values_in_files
        self.assertEqual(expected_dict, dict_in_loader)
