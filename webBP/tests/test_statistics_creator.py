import unittest
from filecmp import cmp
from os.path import abspath, dirname, join, exists
from unittest.mock import MagicMock

import os

from copy import deepcopy

from shutil import rmtree

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

    def test_compute_statistics_one_file(self):
        group_id = 54
        test1_id = 13
        test2_id = 14
        file_id = 75
        user_id = 4
        file_name = 'My testing file'

        test1 = Test()
        test1.id = test1_id
        test1.file_id = file_id
        test1.user_id = user_id
        test2 = deepcopy(test1)
        test2.id = test2_id

        def file_dao_side_effect(f_id):
            file = File()
            file.id = f_id
            file.user_id = user_id
            file.name = file_name
            file.file_system_path = join('users', str(user_id), 'files', str(file_id))
            file.hash = 'ABCD456'
            return file

        def result_dao_side_effect(test):
            return abspath(join(this_dir, 'users', str(user_id), 'tests_results', str(test.id)))

        def nist_dao_side_effect(test):
            nist_param = NistParam()
            if test.id == test1_id:
                nist_param.test_number = 2
            else:
                nist_param.test_number = 3
            return nist_param

        self.stat_creator.group_dao.get_tests_for_group = MagicMock(return_value=[test1, test2])
        self.stat_creator.file_dao.get_file_by_id = MagicMock(side_effect=file_dao_side_effect)
        self.stat_creator.results_dao.get_path_for_test = MagicMock(side_effect=result_dao_side_effect)
        self.stat_creator.nist_dao.get_nist_param_for_test = MagicMock(side_effect=nist_dao_side_effect)

        self.stat_creator.compute_statistics(group_id, user_id)
        group_dir = join(this_dir, 'users', str(user_id), 'groups', str(group_id))
        created_file = join(group_dir, 'grp_' + str(group_id) + '_f_' + str(file_id))
        self.assertTrue(exists(created_file))

        header_dir = join(this_dir, '..', 'nist_statistics', 'templates')
        with open(join(header_dir, 'template1.txt'), 'r') as f:
            header = f.read()
        with open(join(header_dir, 'template2.txt'), 'r') as f:
            header += ' '.join(f.read().rsplit(os.linesep))
            header += '<'
            header += file_name
            header += '>'
            header += os.linesep
        with open(join(header_dir, 'template3.txt'), 'r') as f:
            header += f.read()

        expected_line = '  1   0   2   1   1   1   1   0   2   1  0.000000 *   10/10 *    Block Frequency'
        content = header + expected_line + os.linesep
        expected_line = '  0   2   1   0   0   2   1   0   3   1  0.000000 *   10/10 *    Cumulative Sums'
        content += expected_line + os.linesep
        expected_line = '  0   1   1   0   4   1   0   2   1   0  0.000000 *   10/10 *    Cumulative Sums'
        content += expected_line + os.linesep

        with open(created_file, 'r') as f:
            file_content = f.read()
        with open('/home/jozef/Plocha/foo.txt', 'w') as f:
            f.write(content)

        self.assertEqual(content, file_content, 'Generated file content does not match the expected one')

        os.remove(created_file)
        rmtree(group_dir)
