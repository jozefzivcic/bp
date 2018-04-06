import re
import unittest
from filecmp import cmp
from os.path import abspath, dirname, join, exists
from unittest.mock import MagicMock, patch

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
working_dir = join(this_dir, 'working_dir_stat_creator')


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
        if not exists(working_dir):
            os.mkdir(working_dir)

    def tearDown(self):
        if os.path.exists(working_dir):
            rmtree(working_dir)

    def test_prepare_file(self):
        file = File()
        file.id = self.file1_id
        file.name = self.file_name

        test_id = 456
        self.stat_creator.prepare_file(working_dir, test_id, file)
        another_file = join(sample_files_dir, 'header_test_file.txt')

        expected = join(working_dir, 'report_for_file_id_{}_and_first_test_id_{}.txt'.format(self.file1_id, test_id))
        self.assertTrue(cmp(expected, another_file), 'Files are not the same')

    def test_append_lines_frequency(self):
        test = Test()
        test.id = self.test1_id

        nist_param = NistParam()
        nist_param.test_id = self.test1_id
        nist_param.length = 10000
        nist_param.test_number = 1
        nist_param.streams = 10

        self.stat_creator.results_dao.get_path_for_test = MagicMock(return_value=
                                                                    join(sample_files_dir, 'users', '4',
                                                                         'tests_results',
                                                                         '13'))
        self.stat_creator.nist_dao.get_nist_param_for_test = MagicMock(return_value=nist_param)

        file_path = join(working_dir, 'some_file.txt')
        self.stat_creator.append_lines_for_test(file_path, test)
        expected_line = '  1   0   2   1   1   1   1   0   2   1 ' + ' 0.911413   ' + ' 0.934601   ' + \
                        '1.0000    Frequency'
        expected_line += os.linesep
        with open(file_path, 'r') as f:
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

        ret = self.stat_creator.compute_statistics(self.group_id, working_dir)
        expected_file = join(working_dir, 'report_for_file_id_{}_and_first_test_id_{}.txt'
                             .format(self.file1_id, self.test1_id))
        self.assertEqual(1, len(ret))
        self.assertEqual(expected_file, ret[self.file1_id])
        self.assertTrue(exists(expected_file))

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
        content += expected_line + os.linesep

        end = '\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n' \
              'The minimum pass rate for each statistical test with the exception of the\n' \
              'random excursion (variant) test is approximately = 0.895607 for a\n' \
              'sample size = 10 binary sequences.\n\n' \
              'For further guidelines construct a probability table using the MAPLE program\n' \
              'provided in the addendum section of the documentation.\n' \
              '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
        content += end

        with open(expected_file, 'r') as f:
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

        ret = self.stat_creator.compute_statistics(self.group_id, working_dir)
        expected_file1 = join(working_dir, 'report_for_file_id_{}_and_first_test_id_{}.txt'
                              .format(self.file1_id, self.test1_id))
        expected_file2 = join(working_dir, 'report_for_file_id_{}_and_first_test_id_{}.txt'
                              .format(self.file2_id, self.test2_id))
        self.assertEqual(2, len(ret))
        self.assertEqual(expected_file1, ret[self.file1_id])
        self.assertEqual(expected_file2, ret[self.file2_id])
        self.assertTrue(exists(expected_file1))
        self.assertTrue(exists(expected_file2))

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
        content = header + expected_line + os.linesep + end

        with open(expected_file1, 'r') as f:
            file_content = f.read()

        self.assertEqual(content, file_content, 'Generated file content does not match the expected one')

        expected_line = '  0   2   1   0   0   2   1   0   3   1  0.350485    0.329340   1.0000    Cumulative Sums'
        content = header + expected_line + os.linesep
        expected_line = '  0   1   1   0   4   1   0   2   1   0  0.122325    0.400829   1.0000    Cumulative Sums'
        content += expected_line + os.linesep + end

        with open(expected_file2, 'r') as f:
            file_content = f.read()

        self.assertEqual(content, file_content, 'Generated file content does not match the expected one')

    @patch('managers.dbtestmanager.DBTestManager.get_tests_by_id_list', return_value='return value')
    @patch('nist_statistics.statistics_creator.StatisticsCreator.create_stats_for_tests', return_value='value 2')
    def test_create_stats_for_test_ids(self, f_create_stats, f_get_tests):
        test_ids = [1, 2, 3]
        alpha = 0.456
        ret = self.stat_creator.create_stats_for_tests_ids(test_ids, working_dir, alpha)
        self.assertEqual('value 2', ret)
        f_get_tests.assert_called_once_with(test_ids)
        f_create_stats.assert_called_once_with('return value', working_dir, alpha)

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


class TestComputeStatisticsMoreData(unittest.TestCase):
    """
    p-values used in this test were produced using the following command:
    ./assess -fast -file data/BBS.dat -tests 010000000001100 -fileoutput -binary -streams 15
    1000000 -defaultpar
    """

    def nist_dao_side_effect(self, test):
        nist_param = NistParam()
        nist_param.streams = 15
        if test.id == self.test1.id:
            nist_param.test_number = 2
        elif test.id == self.test2.id:
            nist_param.test_number = 12
        elif test.id == self.test3.id:
            nist_param.test_number = 13
        else:
            raise RuntimeError('Unsupported option')
        return nist_param

    def mock_func(self, func_name, side_effect):
        patcher = patch(func_name, side_effect=side_effect)
        self.addCleanup(patcher.stop)
        patcher.start()

    def mock(self):
        self.mock_func('managers.groupmanager.GroupManager.get_tests_for_group',
                       lambda g_id: [self.test1, self.test2, self.test3])
        self.mock_func('managers.groupmanager.GroupManager.set_statistics_computed',
                       lambda g_id: True)
        self.mock_func('managers.filemanager.FileManager.get_file_by_id', lambda f_id: self.file)
        self.mock_func('managers.resultsmanager.ResultsManager.get_path_for_test',
                       lambda test: abspath(join(sample_files_dir, 'users', str(self.user_id), 'tests_results',
                                                 str(test.id))))
        self.mock_func('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                       self.nist_dao_side_effect)

    def setUp(self):
        self.mock()
        storage_mock = MagicMock(path_to_users_dir=join(sample_files_dir, 'users'), groups='groups')
        self.stat_creator = StatisticsCreator(None, storage_mock)
        self.user_id = 4
        self.group_id = 456

        self.file = File()
        self.file.id = 852
        self.file.user_id = self.user_id
        self.file.name = 'TestingFileName.txt'
        self.file.file_system_path = join('users', str(self.user_id), 'files', str(852))
        self.file.hash = 'ABCD456'

        self.test1 = Test(102, self.file.id, self.user_id, 0, 'nist')
        self.test2 = Test(103, self.file.id, self.user_id, 0, 'nist')
        self.test3 = Test(104, self.file.id, self.user_id, 0, 'nist')

        if not exists(working_dir):
            os.mkdir(working_dir)

    def tearDown(self):
        if os.path.exists(working_dir):
            rmtree(working_dir)

    def test_compute_statistics_complex(self):
        exp = '------------------------------------------------------------------------------\n' \
              'RESULTS FOR THE UNIFORMITY OF P-VALUES AND THE PROPORTION OF PASSING SEQUENCES\n' \
              '------------------------------------------------------------------------------\n' \
              '   generator is <{}>\n' \
              '------------------------------------------------------------------------------\n' \
              ' C1  C2  C3  C4  C5  C6  C7  C8  C9 C10  P-VALUE  P-value(KS) PROPORTION  STATISTICAL TEST\n' \
              '------------------------------------------------------------------------------\n' \
              '  2   1   2   1   2   3   0   2   1   1  0.437274    0.675978   1.0000    Block Frequency\n' \
              '  1   1   1   2   0   0   2   1   2   0  0.739918    0.971717   1.0000    Random Excursions\n' \
              '  2   1   3   3   0   1   0   0   0   0  0.122325    0.006948   1.0000    Random Excursions\n' \
              '  1   0   0   3   0   0   3   2   0   1  0.122325    0.516211   1.0000    Random Excursions\n' \
              '  0   0   0   1   1   2   2   1   1   2  0.739918    0.070746   1.0000    Random Excursions\n' \
              '  0   1   0   1   1   0   1   1   2   3  0.534146    0.070001   1.0000    Random Excursions\n' \
              '  2   1   1   0   0   0   2   1   3   0  0.350485    0.351565   1.0000    Random Excursions\n' \
              '  1   0   1   1   0   1   3   0   1   2  0.534146    0.541305   1.0000    Random Excursions\n' \
              '  0   0   2   1   0   2   0   1   2   2  0.534146    0.454285   1.0000    Random Excursions\n' \
              '  1   0   0   3   2   0   0   0   0   4  0.017912    0.226128   1.0000    Random Excursions Variant\n' \
              '  1   0   0   1   2   1   2   1   2   0  0.739918    0.431003   1.0000    Random Excursions Variant\n' \
              '  1   0   0   0   2   2   2   1   1   1  0.739918    0.095168   1.0000    Random Excursions Variant\n' \
              '  1   0   0   0   0   2   5   0   2   0  0.004301    0.049755   1.0000    Random Excursions Variant\n' \
              '  1   0   0   1   2   2   4   0   0   0  0.066882    0.267220   1.0000    Random Excursions Variant\n' \
              '  1   0   3   0   2   3   1   0   0   0  0.122325    0.115492   0.9000    Random Excursions Variant\n' \
              '  1   1   1   0   3   3   1   0   0   0  0.213309    0.094227   1.0000    Random Excursions Variant\n' \
              '  0   1   1   0   4   0   1   2   0   1  0.122325    0.547756   1.0000    Random Excursions Variant\n' \
              '  0   0   2   0   1   2   1   1   2   1  0.739918    0.567491   1.0000    Random Excursions Variant\n' \
              '  0   0   0   0   1   1   1   3   2   2  0.350485    0.009777   1.0000    Random Excursions Variant\n' \
              '  0   1   1   0   2   1   1   0   1   3  0.534146    0.344998   1.0000    Random Excursions Variant\n' \
              '  1   1   0   1   0   0   3   4   0   0  0.035174    0.089265   1.0000    Random Excursions Variant\n' \
              '  0   3   1   0   0   1   1   1   2   1  0.534146    0.775124   1.0000    Random Excursions Variant\n' \
              '  2   0   2   0   2   0   1   1   0   2  0.534146    0.964988   1.0000    Random Excursions Variant\n' \
              '  2   1   1   1   0   0   1   1   1   2  0.911413    0.921317   1.0000    Random Excursions Variant\n' \
              '  0   2   2   2   0   0   0   0   1   3  0.213309    0.312624   1.0000    Random Excursions Variant\n' \
              '  1   0   1   0   2   1   1   2   0   2  0.739918    0.743081   1.0000    Random Excursions Variant\n' \
              '  0   1   1   1   1   0   2   2   1   1  0.911413    0.699618   1.0000    Random Excursions Variant\n' \
              '\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n' \
              'The minimum pass rate for each statistical test with the exception of the\n' \
              'random excursion (variant) test is approximately = 0.912929 for a\n' \
              'sample size = 15 binary sequences.\n\n' \
              'The minimum pass rate for the random excursion (variant) test\n' \
              'is approximately 0.895607 for a sample size = 10 binary sequences.\n\n' \
              'For further guidelines construct a probability table using the MAPLE program\n' \
              'provided in the addendum section of the documentation.\n' \
              '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -' \
            .format(self.file.name)
        ret = self.stat_creator.compute_statistics(self.group_id, working_dir)
        expected_file = join(working_dir, 'report_for_file_id_{}_and_first_test_id_{}.txt'
                             .format(self.file.id, self.test1.id))
        self.assertEqual(1, len(ret))
        self.assertEqual(expected_file, ret[self.file.id])
        self.assertTrue(exists(expected_file))
        with open(ret[self.file.id], 'r') as f:
            file_content = f.read()
        self.assert_content_equal(exp, file_content)

    def assert_content_equal(self, exp: str, ret: str):
        exp_split = exp.splitlines()
        ret_split = ret.splitlines()
        self.assertEqual(len(exp_split), len(ret_split))
        for i in range(7):  # compare header of report
            self.assertEqual(exp_split[i], ret_split[i])
        i = 7
        while i < len(exp_split) and exp_split[i] != '':  # compare content of report
            g1 = self.parse_line(exp_split[i])
            g2 = self.parse_line(ret_split[i])
            self.compare_groups(g1, g2)
            i += 1

        while i < len(exp_split):  # compare end of report
            self.assertEqual(exp_split[i], ret_split[i])
            i += 1

    def parse_line(self, line: str) -> tuple:
        pattern = '^\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)' \
                  '\s+(\d*[.,]?\d*)\s+(\d*[.,]?\d*)\s+(\d*[.,]?\d*)\s+(\w+\s?\w+\s?\w+?)$'
        m = re.match(pattern, line)
        return tuple(m.groups())

    def compare_groups(self, expected: tuple, ret: tuple):
        for i in range(10):
            self.assertEqual(expected[i], ret[i])
        self.assertAlmostEqual(float(expected[10]), float(ret[10]), places=6)  # p-value
        self.assertAlmostEqual(float(expected[11]), float(ret[11]), places=5)  # p-value (KS)
        self.assertAlmostEqual(float(expected[12]), float(ret[12]), places=6)  # proportions
        self.assertEqual(expected[13], ret[13])  # name of the test
