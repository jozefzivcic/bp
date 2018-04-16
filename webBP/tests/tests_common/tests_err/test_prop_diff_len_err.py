from configparser import ConfigParser
from unittest import TestCase

from common.error.prop_diff_len_err import DiffPValuesLenErr


class TestPropDiffLenErr(TestCase):
    def test_init_raises(self):
        with self.assertRaises(ValueError) as ex:
            DiffPValuesLenErr(10, 10)
        self.assertEqual('Expected and actual lengths are the same: 10', str(ex.exception))

    def test_get_message(self):
        data_dict = {'ErrTemplates': {'PropDiffLen': 'expected: {} ret: {}'}}
        expected = 'expected: 10 ret: 4'
        cfg = ConfigParser()
        cfg.read_dict(data_dict)
        err = DiffPValuesLenErr(10, 4)
        ret = err.get_message(cfg)
        self.assertEqual(expected, ret)

    def test_not_equal(self):
        e1 = DiffPValuesLenErr(6, 7)
        e2 = DiffPValuesLenErr(5, 7)
        self.assertFalse(e1 == e2)
        self.assertTrue(e1 != e2)

        e1 = DiffPValuesLenErr(7, 5)
        e2 = DiffPValuesLenErr(7, 6)
        self.assertFalse(e1 == e2)
        self.assertTrue(e1 != e2)

    def test_are_equal(self):
        e1 = DiffPValuesLenErr(7, 8)
        e2 = DiffPValuesLenErr(7, 8)
        self.assertTrue(e1 == e2)
        self.assertFalse(e1 != e2)
