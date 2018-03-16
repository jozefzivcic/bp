from configparser import ConfigParser
from unittest import TestCase

from common.info.test_dep_unif_info import TestDepUnifInfo


class TestOfTestDepUnifInfo(TestCase):
    def test_get_message(self):
        cfg = ConfigParser()
        cfg.read_dict({'InfoTemplates': {'TestDepUnifInfoT': '{} fulfilled',
                                         'TestDepUnifInfoF': '{} not-fulfilled'}})

        info = TestDepUnifInfo(0.756, True)
        message = info.get_message(cfg)
        expected = '0.756 fulfilled'
        self.assertEqual(expected, message)

        info = TestDepUnifInfo(0.756, False)
        message = info.get_message(cfg)
        expected = '0.756 not-fulfilled'
        self.assertEqual(expected, message)
