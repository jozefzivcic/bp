import unittest
from os.path import dirname, abspath, join
from unittest.mock import MagicMock

from nist_statistics.p_value_provider import PValueProvider
from models.test import Test

this_dir = dirname(abspath(__file__))


class PValueProviderTest(unittest.TestCase):
    def setUp(self):
        self.provider = PValueProvider(None)

    def test_load_p_values_from_one_file(self):
        expected_p_values = [0.857153, 0.298340, 0.674485, 0.078408, 0.200545, 0.888660, 0.471525, 0.920344, 0.357573,
                             0.509254]
        test = Test()
        dir_with_results = join(this_dir, 'users', '4', 'tests_results', '13')
        self.provider.result_dao.get_path_for_test = MagicMock(return_value=dir_with_results)
        ret = self.provider.get_p_values_for_test(test)
        self.assertEqual(expected_p_values , ret, 'Loaded p_values from file are different than the expected ones')

    def test_load_p_values_from_two_files(self):
        expected_p_values = [0.593063, 0.584171, 0.849583, 0.131536, 0.206201, 0.911652, 0.882140, 0.814758, 0.160236,
                             0.684836, 0.759852, 0.483106, 0.475200, 0.131536, 0.252025, 0.796727, 0.467379, 0.897326,
                             0.483106, 0.532261]
        test = Test()
        dir_with_results = join(this_dir, 'users', '4', 'tests_results', '14')
        self.provider.result_dao.get_path_for_test = MagicMock(return_value=dir_with_results)
        ret = self.provider.get_p_values_for_test(test)
        self.assertEqual(expected_p_values , ret, 'Loaded p_values from file are different than the expected ones')

    def test_load_p_values_from_one_file_with_order(self):
        expected_p_values = [[1, 0.857153], [2, 0.298340], [3, 0.674485], [4,0.078408], [5, 0.200545], [6, 0.888660],
                             [7, 0.471525], [8, 0.920344], [9, 0.357573], [10, 0.509254]]
        test = Test()
        dir_with_results = join(this_dir, 'users', '4', 'tests_results', '13')
        self.provider.result_dao.get_path_for_test = MagicMock(return_value=dir_with_results)
        ret = self.provider.get_p_values_with_order_for_test(test)
        self.assertEqual(expected_p_values , ret, 'Loaded p_values from file are different than the expected ones')

    def test_load_p_values_from_two_files_with_order(self):
        expected_p_values = [[1, 0.593063], [2, 0.584171], [3, 0.849583], [4, 0.131536], [5, 0.206201], [6, 0.911652],
                             [7, 0.882140], [8, 0.814758], [9, 0.160236], [10, 0.684836], [11, 0.759852],
                             [12, 0.483106], [13, 0.475200], [14, 0.131536], [15, 0.252025], [16, 0.796727],
                             [17, 0.467379], [18, 0.897326], [19, 0.483106], [20, 0.532261]]
        test = Test()
        dir_with_results = join(this_dir, 'users', '4', 'tests_results', '14')
        self.provider.result_dao.get_path_for_test = MagicMock(return_value=dir_with_results)
        ret = self.provider.get_p_values_with_order_for_test(test)
        self.assertEqual(expected_p_values , ret, 'Loaded p_values from file are different than the expected ones')
