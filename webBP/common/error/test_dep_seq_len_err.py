from configparser import ConfigParser

from common.error.err import Err
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType


class TestDepSeqLenErr(Err):
    def __init__(self, seq1: PValueSequence, seq1_len: int, seq2: PValueSequence, seq2_len: int):
        if seq1_len == seq2_len:
            raise ValueError('Sequences cannot have the same length for this object type {}, {}'
                             .format(seq1_len, seq2_len))
        self.seq1 = seq1
        self._seq1_len = seq1_len
        self.seq2 = seq2
        self._seq2_len = seq2_len

    def get_message(self, texts: ConfigParser) -> str:
        seq1_str = self.get_seq_messge(texts, self.seq1)
        seq2_str = self.get_seq_messge(texts, self.seq2)
        return texts.get('ErrTemplates', 'TestDepDifferentLen')\
            .format(seq1_str, seq2_str, self._seq1_len, self._seq2_len)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.seq1 == other.seq1 and self._seq1_len == other._seq1_len and self.seq2 == other.seq2 and \
               self._seq2_len == other._seq2_len

    def get_seq_messge(self, texts: ConfigParser, seq: PValueSequence) -> str:
        test_id_str = texts.get('General', 'TestId')
        if seq.p_values_file == PValuesFileType.RESULTS:
            file_spec = texts.get('General', 'Results')
        elif seq.p_values_file == PValuesFileType.DATA:
            file_spec = texts.get('General', 'Data')
            file_spec = '{} {}'.format(file_spec, seq.data_num)
        else:
            raise RuntimeError('Unknown file type {}'.format(seq.p_values_file))
        return '{}: {} {}'.format(test_id_str, seq.test_id, file_spec)
