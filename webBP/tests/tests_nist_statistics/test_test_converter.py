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

    def test_convert(self):
        test1 = Test()
        test1.id = 5
        test1.file_id = file1_id
        test1.user_id = user_id
        test1.time_of_add = time_of_add
        test1.test_table = test_table

        test2 = copy.deepcopy(test1)
        test2.id = 6

        test3 = copy.deepcopy(test1)
        test3.id = 14
        test3.file_id = file2_id

        test_arr = [test1, test2, test3]

        returned_dict = self.test_converter.get_tests_for_files(test_arr)

        expected_dict = {file1_id: [test1, test2], file2_id: [test3]}

        self.assertDictEqual(returned_dict, expected_dict, 'Returned and expected dictionaries are not the same')