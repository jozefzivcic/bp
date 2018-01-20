from unittest import TestCase

from p_value_processing.data_file_error import DataFileError
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14
from p_value_processing.p_values_dto import PValuesDto


class TestPValuesDtoOnTest13(TestCase):
    def setUp(self):
        self.dto = PValuesDto(dict_for_test_13)

    def test_results(self):
        expected_p_values = dict_for_test_13['results']
        ret = self.dto.get_results_p_values()
        self.assertEqual(expected_p_values, ret)

    def test_data_raise_exception(self):
        data_num = 1
        with self.assertRaises(ValueError) as context:
            self.dto.get_data_p_values(data_num)
        self.assertTrue(str(data_num) in str(context.exception))

    def test_get_data_indices(self):
        with self.assertRaises(DataFileError) as context:
            self.dto.get_data_files_indices()
        self.assertTrue('No data file', str(context.exception))


class TestPValuesDtoOnTest14(TestCase):
    def setUp(self):
        self.dto = PValuesDto(dict_for_test_14)

    def test_results(self):
        expected_p_values = dict_for_test_14['results']
        ret = self.dto.get_results_p_values()
        self.assertEqual(expected_p_values, ret)

    def test_data_1(self):
        expected_p_values = dict_for_test_14['data1']
        ret = self.dto.get_data_p_values(1)
        self.assertEqual(expected_p_values, ret)

    def test_data_2(self):
        expected_p_values = dict_for_test_14['data2']
        ret = self.dto.get_data_p_values(2)
        self.assertEqual(expected_p_values, ret)

    def test_data_3(self):
        data_num = 3
        with self.assertRaises(ValueError) as context:
            self.dto.get_data_p_values(data_num)
        self.assertTrue(str(data_num) in str(context.exception))

    def test_data_0(self):
        data_num = 0
        with self.assertRaises(ValueError) as context:
            self.dto.get_data_p_values(data_num)
        self.assertTrue(str(data_num) in str(context.exception))

    def test_data_not_number(self):
        data_num = 'string'
        with self.assertRaises(ValueError) as context:
            self.dto.get_data_p_values(data_num)
        self.assertTrue(str(data_num) in str(context.exception))

    def test_data_indices(self):
        expected = [1, 2]
        ret = self.dto.get_data_files_indices()
        self.assertEqual(expected, ret)


class TestPValuesDto(TestCase):
    def test_data_indices_sorted(self):
        p_values_dict = {}
        num_of_iterations = PValuesDto.max_num_of_data_files
        expected = []
        for i in range(1, num_of_iterations + 1):
            key = 'data' + str(i)
            p_values_dict[key] = []
            expected.append(i)

        dto = PValuesDto(p_values_dict)
        ret = dto.get_data_files_indices()
        self.assertEqual(expected, ret)

    def test_too_many_data_files(self):
        p_values_dict = {}
        num_of_iterations = PValuesDto.max_num_of_data_files + 1
        for i in range(1, num_of_iterations + 1):
            key = 'data' + str(i)
            p_values_dict[key] = []

        with self.assertRaises(DataFileError) as context:
            dto = PValuesDto(p_values_dict)
        self.assertEqual('Too many data files. Allowed maximum is ' + str(PValuesDto.max_num_of_data_files),
                         str(context.exception))

    def test_has_data_files_true(self):
        dto = PValuesDto(dict_for_test_14)
        self.assertTrue(dto.has_data_files())

    def test_has_data_files_false(self):
        dto = PValuesDto(dict_for_test_13)
        self.assertFalse(dto.has_data_files())

    def test_obj_are_equal(self):
        my_dict = {'results': [0.1, 0.2, 0.456]}
        dto1 = PValuesDto(my_dict)
        dto2 = PValuesDto(my_dict)
        self.assertTrue(dto1 == dto2)
        self.assertFalse(dto1 != dto2)

    def test_obj_are_not_equal(self):
        my_dict1 = {'results': [0.1, 0.2, 0.456]}
        my_dict2 = {'results': [0.1, 0.456, 0.2]}
        dto1 = PValuesDto(my_dict1)
        dto2 = PValuesDto(my_dict2)
        self.assertFalse(dto1 == dto2)
        self.assertTrue(dto1 != dto2)
