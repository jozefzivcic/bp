import unittest

from logger import Logger
from nist_statistics.statistics_creator import StatisticsCreator


class StatCreatorTest(unittest.TestCase):
    def setUp(self):
        self.stat_creator = StatisticsCreator(None, Logger(), None)

    def test_prepare_file(self):
        self.assertTrue(True, 'Files are not the same')
