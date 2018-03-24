from configparser import ConfigParser
from unittest import TestCase

from common.error.test_dep_seq_len_err import TestDepSeqLenErr
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType


class TestOfTestDepSeqLenErr(TestCase):
    def test_same_len(self):
        with self.assertRaises(ValueError) as ex:
            TestDepSeqLenErr(PValueSequence(1, PValuesFileType.RESULTS), 5,
                             PValueSequence(2, PValuesFileType.DATA, 2), 5)
        self.assertEqual('Sequences cannot have the same length for this object type 5, 5',
                         str(ex.exception))

    def test_get_message(self):
        cfg = ConfigParser()
        cfg.read_dict({'General': {'Results': 'results', 'Data': 'data', 'TestId': 'test_id'},
                       'ErrTemplates': {'TestDepDifferentLen': 'seq {} and {} different length {} {}'}})

        err = TestDepSeqLenErr(PValueSequence(1, PValuesFileType.RESULTS), 5,
                               PValueSequence(2, PValuesFileType.DATA, 2), 4)
        expected = 'seq test_id: 1 results and test_id: 2 data 2 different length 5 4'
        ret = err.get_message(cfg)
        self.assertEqual(expected, ret)
