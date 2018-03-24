from p_value_processing.p_value_sequence import PValueSequence


class DifferentListsSizeError(Exception):
    def __init__(self, message: str, seq1: PValueSequence, len1: int, seq2: PValueSequence, len2: int):
        super(DifferentListsSizeError, self).__init__(message)
        self.seq1 = seq1
        self.len1 = len1
        self.seq2 = seq2
        self.len2 = len2
