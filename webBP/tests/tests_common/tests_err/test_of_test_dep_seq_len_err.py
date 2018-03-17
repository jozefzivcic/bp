from configparser import ConfigParser
from unittest import TestCase

from common.error.test_dep_seq_len_err import TestDepSeqLenErr


class TestOfTestDepSeqLenErr(TestCase):
    def test_same_len(self):
        with self.assertRaises(ValueError) as ex:
            TestDepSeqLenErr(5, 5)
        self.assertEqual('Sequences cannot have the same length for this object type 5, 5',
                         str(ex.exception))

    def test_get_message(self):
        cfg = ConfigParser()
        cfg.read_dict({'ErrTemplates': {'TestDepDifferentLen': 'different length {} {}'}})

        err = TestDepSeqLenErr(5, 4)
        expected = 'different length 5 4'
        ret = err.get_message(cfg)
        self.assertEqual(expected, ret)
