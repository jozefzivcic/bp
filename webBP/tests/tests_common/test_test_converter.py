from unittest import TestCase

import datetime

import copy

from common.test_converter import TestConverter
from models.test import Test

file1_id = 4
file2_id = 5
user_id = 78
time_of_add = datetime.datetime(2012, 12, 4, 19, 51, 25, 362455)
test_table = 'nist'


class TestTestConverter(TestCase):
    def setUp(self):
        self.test_converter = TestConverter()
        self.test1 = Test()
        self.test1.id = 5
        self.test1.file_id = file1_id
        self.test1.user_id = user_id
        self.test1.time_of_add = time_of_add
        self.test1.test_table = test_table

        self.test2 = copy.deepcopy(self.test1)
        self.test2.id = 6

        self.test3 = copy.deepcopy(self.test1)
        self.test3.id = 14
        self.test3.file_id = file2_id

    def test_convert(self):
        test_arr = [self.test1, self.test2, self.test3]
        returned_dict = self.test_converter.get_tests_for_files(test_arr)
        expected_dict = {file1_id: [self.test1, self.test2], file2_id: [self.test3]}
        self.assertDictEqual(returned_dict, expected_dict, 'Returned and expected dictionaries are not the same')

    def test_get_test_ids_for_files(self):
        test_arr = [self.test1, self.test2, self.test3]
        returned_dict = self.test_converter.get_test_ids_for_files(test_arr)
        expected_dict = {file1_id: [self.test1.id, self.test2.id], file2_id: [self.test3.id]}
        self.assertDictEqual(returned_dict, expected_dict, 'Returned and expected dictionaries are not the same')
