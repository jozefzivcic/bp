import unittest
from filecmp import cmp
from os.path import abspath, dirname, join, exists
from unittest.mock import MagicMock

import os

from copy import deepcopy

from shutil import rmtree

from enums.nist_test_type import NistTestType
from nist_statistics.statistics_creator import StatisticsCreator
from models.file import File
from models.nistparam import NistParam
from models.test import Test

this_dir = dirname(abspath(__file__))
sample_files_dir = join(this_dir, '..', 'sample_files_for_tests')


class StatCreatorTest(unittest.TestCase):

    def file_dao_side_effect(self, f_id):
        file = File()
        file.id = f_id
        file.user_id = self.user_id
        file.name = self.file_name
        file.file_system_path = join('users', str(self.user_id), 'files', str(f_id))
        file.hash = 'ABCD456'
        return file

    def result_dao_side_effect(self, test):
        return abspath(join(sample_files_dir, 'users', str(self.user_id), 'tests_results', str(test.id)))

    def nist_dao_side_effect(self, test):
        nist_param = NistParam()
        nist_param.streams = 10
        if test.id == self.test1_id:
            nist_param.test_number = 1
        else:
            nist_param.test_number = 3
        return nist_param

    def setUp(self):
        storage_mock = MagicMock()
        storage_mock.path_to_users_dir = join(sample_files_dir, 'users')
        storage_mock.groups = 'groups'
        self.stat_creator = StatisticsCreator(None, storage_mock)
        self.user_id = 4
        self.group_id = 54
        self.file1_id = 75
        self.file2_id = 87
        self.test1_id = 13
        self.test2_id = 14
        self.file_name = 'TestFile.txt'
        self.group_dir = join(sample_files_dir, 'users', str(self.user_id), 'groups', str(self.group_id))
        self.summary_file1 = join(self.group_dir, 'grp_' + str(self.group_id) + '_f_' + str(self.file1_id))
        self.summary_file2 = join(self.group_dir, 'grp_' + str(self.group_id) + '_f_' + str(self.file2_id))
        if not exists(self.group_dir):
            os.mkdir(self.group_dir)

    def tearDown(self):
        if os.path.exists(self.group_dir):
            rmtree(self.group_dir)

    def test_prepare_file(self):
        file = File()
        file.id = self.file1_id
        file.name = self.file_name

        self.stat_creator.prepare_file(self.group_id, self.user_id, file)
        another_file = join(sample_files_dir, 'header_test_file.txt')

        self.assertTrue(cmp(self.summary_file1, another_file), 'Files are not the same')

    def test_append_lines_frequency(self):
        test = Test()
        test.id = self.test1_id

        nist_param = NistParam()
        nist_param.test_id = self.test1_id
        nist_param.length = 10000
        nist_param.test_number = 1
        nist_param.streams = 10

        self.stat_creator.results_dao.get_path_for_test = MagicMock(return_value=
                                                                    join(sample_files_dir, 'users', '4', 'tests_results',
                                                                         '13'))
        self.stat_creator.nist_dao.get_nist_param_for_test = MagicMock(return_value=nist_param)

        self.stat_creator.append_lines_for_test(self.summary_file1, test)
        expected_line = '  1   0   2   1   1   1   1   0   2   1 ' + ' 0.911413   ' + ' 0.934601   ' + \
                        '1.0000    Frequency'
        expected_line += os.linesep
        with open(self.summary_file1, 'r') as f:
            read_line = f.read()
        self.assertEqual(read_line, expected_line, 'File does not contain a line as expected')

    def test_compute_statistics_one_file(self):
        test1 = Test()
        test1.id = self.test1_id
        test1.file_id = self.file1_id
        test1.user_id = self.user_id
        test2 = deepcopy(test1)
        test2.id = self.test2_id

        self.stat_creator.group_dao.get_tests_for_group = MagicMock(return_value=[test1, test2])
        self.stat_creator.file_dao.get_file_by_id = MagicMock(side_effect=self.file_dao_side_effect)
        self.stat_creator.results_dao.get_path_for_test = MagicMock(side_effect=self.result_dao_side_effect)
        self.stat_creator.nist_dao.get_nist_param_for_test = MagicMock(side_effect=self.nist_dao_side_effect)
        self.stat_creator.group_dao.set_statistics_computed = MagicMock(return_value=True)

        self.stat_creator.compute_statistics(self.group_id, self.user_id)
        self.assertTrue(exists(self.summary_file1))

        header_dir = join(sample_files_dir, '..', '..', 'nist_statistics', 'templates')
        with open(join(header_dir, 'template1.txt'), 'r') as f:
            header = f.read()
        with open(join(header_dir, 'template2.txt'), 'r') as f:
            header += ' '.join(f.read().rsplit(os.linesep))
            header += '<'
            header += self.file_name
            header += '>'
            header += os.linesep
        with open(join(header_dir, 'template3.txt'), 'r') as f:
            header += f.read()

        expected_line = '  1   0   2   1   1   1   1   0   2   1  0.911413    0.934601   1.0000    Frequency'
        content = header + expected_line + os.linesep
        expected_line = '  0   2   1   0   0   2   1   0   3   1  0.350485    0.329340   1.0000    Cumulative Sums'
        content += expected_line + os.linesep
        expected_line = '  0   1   1   0   4   1   0   2   1   0  0.122325    0.400829   1.0000    Cumulative Sums'
        content += expected_line

        end = '\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n' \
              'The minimum pass rate for each statistical test with the exception of the\n' \
              'random excursion (variant) test is approximately = 0.895607 for a\n' \
              'sample size = 10 binary sequences.\n\n' \
              'For further guidelines construct a probability table using the MAPLE program\n' \
              'provided in the addendum section of the documentation.\n' \
              '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
        content += end

        with open(self.summary_file1, 'r') as f:
            file_content = f.read()

        self.assertEqual(content, file_content, 'Generated file content does not match the expected one')

    def test_compute_statistics_two_files(self):
        test1 = Test()
        test1.id = self.test1_id
        test1.file_id = self.file1_id
        test1.user_id = self.user_id
        test2 = deepcopy(test1)
        test2.id = self.test2_id
        test2.file_id = self.file2_id

        self.stat_creator.group_dao.get_tests_for_group = MagicMock(return_value=[test1, test2])
        self.stat_creator.file_dao.get_file_by_id = MagicMock(side_effect=self.file_dao_side_effect)
        self.stat_creator.results_dao.get_path_for_test = MagicMock(side_effect=self.result_dao_side_effect)
        self.stat_creator.nist_dao.get_nist_param_for_test = MagicMock(side_effect=self.nist_dao_side_effect)
        self.stat_creator.group_dao.set_statistics_computed = MagicMock(return_value=True)

        self.stat_creator.compute_statistics(self.group_id, self.user_id)
        self.assertTrue(exists(self.summary_file1))
        self.assertTrue(exists(self.summary_file2))

        header_dir = join(sample_files_dir, '..', '..', 'nist_statistics', 'templates')
        with open(join(header_dir, 'template1.txt'), 'r') as f:
            header = f.read()
        with open(join(header_dir, 'template2.txt'), 'r') as f:
            header += ' '.join(f.read().rsplit(os.linesep))
            header += '<'
            header += self.file_name
            header += '>'
            header += os.linesep
        with open(join(header_dir, 'template3.txt'), 'r') as f:
            header += f.read()

        expected_line = '  1   0   2   1   1   1   1   0   2   1  0.911413    0.934601   1.0000    Frequency'
        end = '\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n' \
              'The minimum pass rate for each statistical test with the exception of the\n' \
              'random excursion (variant) test is approximately = 0.895607 for a\n' \
              'sample size = 10 binary sequences.\n\n' \
              'For further guidelines construct a probability table using the MAPLE program\n' \
              'provided in the addendum section of the documentation.\n' \
              '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
        content = header + expected_line + end

        with open(self.summary_file1, 'r') as f:
            file_content = f.read()

        self.assertEqual(content, file_content, 'Generated file content does not match the expected one')

        expected_line = '  0   2   1   0   0   2   1   0   3   1  0.350485    0.329340   1.0000    Cumulative Sums'
        content = header + expected_line + os.linesep
        expected_line = '  0   1   1   0   4   1   0   2   1   0  0.122325    0.400829   1.0000    Cumulative Sums'
        content += expected_line + end

        with open(self.summary_file2, 'r') as f:
            file_content = f.read()

        self.assertEqual(content, file_content, 'Generated file content does not match the expected one')

    def test_add_test_for_file(self):
        nist_param = MagicMock(test_number=1)
        self.stat_creator.add_test_for_file(nist_param)
        expected = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(expected, self.stat_creator.tests_in_file)

        nist_param = MagicMock(test_number=15)
        self.stat_creator.add_test_for_file(nist_param)
        expected = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        self.assertEqual(expected, self.stat_creator.tests_in_file)

        nist_param = MagicMock(test_number=12)
        self.stat_creator.add_test_for_file(nist_param)
        expected = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        self.assertEqual(expected, self.stat_creator.tests_in_file)

        nist_param = MagicMock(test_number=12)
        self.stat_creator.add_test_for_file(nist_param)
        expected = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1]
        self.assertEqual(expected, self.stat_creator.tests_in_file)

    def test_reset(self):
        self.stat_creator.tests_in_file = [1, 2, 3]
        self.stat_creator.general_sample_size = 456
        self.stat_creator.random_excursion_sample_size = 654

        self.stat_creator.reset()
        self.assertEqual([0 for _ in range(15)], self.stat_creator.tests_in_file)
        self.assertEqual(0, self.stat_creator.general_sample_size)
        self.assertEqual(0, self.stat_creator.random_excursion_sample_size)

    def test_contains_test(self):
        for t_type in NistTestType:
            self.assertFalse(self.stat_creator.contains_test(t_type))

        self.stat_creator.tests_in_file[0] = 1
        self.assertTrue(self.stat_creator.contains_test(NistTestType.TEST_FREQUENCY))

        self.stat_creator.tests_in_file[0] = 2
        self.assertTrue(self.stat_creator.contains_test(NistTestType.TEST_FREQUENCY))
        self.assertFalse(self.stat_creator.contains_test(NistTestType.TEST_BLOCK_FREQUENCY))
