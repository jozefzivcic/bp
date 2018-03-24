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

    def test_get_message_p_value_precision(self):
        cfg = ConfigParser()
        cfg.read_dict({'InfoTemplates': {'TestDepUnifInfoT': '{} fulfilled',
                                         'TestDepUnifInfoF': '{} not-fulfilled'}})

        info = TestDepUnifInfo(0.756456456, True)
        message = info.get_message(cfg)
        expected = '0.756456 fulfilled'
        self.assertEqual(expected, message)

    def test_get_message_p_value_rounded(self):
        cfg = ConfigParser()
        cfg.read_dict({'InfoTemplates': {'TestDepUnifInfoT': '{} fulfilled',
                                         'TestDepUnifInfoF': '{} not-fulfilled'}})

        info = TestDepUnifInfo(0.4564565789159, True)
        message = info.get_message(cfg)
        expected = '0.456457 fulfilled'
        self.assertEqual(expected, message)

    def test_get_message_small_p_value_round_down(self):
        cfg = ConfigParser()
        cfg.read_dict({'InfoTemplates': {'TestDepUnifInfoT': '{} fulfilled',
                                         'TestDepUnifInfoF': '{} not-fulfilled'}})

        info = TestDepUnifInfo(0.000000456, True)
        message = info.get_message(cfg)
        expected = '0 fulfilled'
        self.assertEqual(expected, message)

    def test_get_message_small_p_value_round_up(self):
        cfg = ConfigParser()
        cfg.read_dict({'InfoTemplates': {'TestDepUnifInfoT': '{} fulfilled',
                                         'TestDepUnifInfoF': '{} not-fulfilled'}})

        info = TestDepUnifInfo(0.000000556, True)
        message = info.get_message(cfg)
        expected = '0.000001 fulfilled'
        self.assertEqual(expected, message)
