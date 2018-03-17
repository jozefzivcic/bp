from configparser import ConfigParser

from common.error.err import Err


class TestDepSeqLenErr(Err):
    def __init__(self, seq1_len: int, seq2_len: int):
        if seq1_len == seq2_len:
            raise ValueError('Sequences cannot have the same length for this object type {}, {}'
                             .format(seq1_len, seq2_len))
        self._seq1_len = seq1_len
        self._seq2_len = seq2_len

    def get_message(self, texts: ConfigParser):
        return texts.get('ErrTemplates', 'TestDepDifferentLen').format(self._seq1_len, self._seq2_len)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self._seq1_len == other._seq1_len and self._seq2_len == other._seq2_len
