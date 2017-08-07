import unittest
from filecmp import cmp
from os.path import abspath, dirname, join
from unittest.mock import MagicMock

from logger import Logger
from nist_statistics.statistics_creator import StatisticsCreator
from models.file import File


class StatCreatorTest(unittest.TestCase):
    def setUp(self):
        this_dir = dirname(abspath(__file__))
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
        this_dir = dirname(abspath(__file__))
        created_file = join(this_dir, 'users', str(user_id), 'groups', str(group_id), 'grp_' + str(group_id) + '_f_' +
                            str(file.id))
        another_file = join(this_dir,   'test_files', 'header_test_file.txt')
        self.assertTrue(cmp(created_file, another_file), 'Files are not the same')
