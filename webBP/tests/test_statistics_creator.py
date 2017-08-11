import unittest
from filecmp import cmp
from os.path import abspath, dirname, join
from unittest.mock import MagicMock

import os

from logger import Logger
from nist_statistics.statistics_creator import StatisticsCreator
from models.file import File
from models.nistparam import NistParam
from models.test import Test

this_dir = dirname(abspath(__file__))


class StatCreatorTest(unittest.TestCase):
    def setUp(self):
        storage_mock = MagicMock()
        storage_mock.path_to_users_dir = join(this_dir, 'users')
        storage_mock.groups = 'groups'
        self.stat_creator = StatisticsCreator(None, Logger(), storage_mock)

    def test_prepare_file(self):
        user_id = 4
        group_id = 5
        file = File()
        file.id = 6
        file.name = 'TestFile.txt'
        self.stat_creator.prepare_file(group_id, user_id, file)
        created_file = join(this_dir, 'users', str(user_id), 'groups', str(group_id), 'grp_' + str(group_id) + '_f_' +
                            str(file.id))
        another_file = join(this_dir, 'test_files', 'header_test_file.txt')
        self.assertTrue(cmp(created_file, another_file), 'Files are not the same')

    def test_append_lines_frequency(self):
        test = Test()
        test.id = 13

        nist_param = NistParam()
        nist_param.test_id = 13
        nist_param.length = 10000
        nist_param.test_number = 1
        nist_param.streams = 10

        self.stat_creator.results_dao.get_path_for_test = MagicMock(return_value=
                                                                    join(this_dir, 'users', '4', 'tests_results',
                                                                         '13'))
        self.stat_creator.nist_dao.get_nist_param_for_test = MagicMock(return_value=nist_param)

        file_name = join(this_dir, 'users', '4', 'groups', '5', 'grp_5_f_7')
        try:
            os.remove(file_name)
        except OSError:
            pass

        self.stat_creator.append_lines_for_test(file_name, test)
        expected_line = '  1   0   2   1   1   1   1   0   2   1  0.000000 *   10/10 *    Frequency'
        with open(file_name, 'r') as f:
            read_line = f.read()
        self.assertEqual(read_line, expected_line, 'File does not contain a line as expected')

        try:
            os.remove(file_name)
        except OSError:
            pass
