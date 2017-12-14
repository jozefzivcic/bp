from unittest import TestCase

from p_value_processing.nist_loader import NistLoader


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

