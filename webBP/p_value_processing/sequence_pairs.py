from p_value_processing.p_value_sequence import PValueSequence


class SequencePairs:
    def __init__(self):
        self._pairs = {}

    def add_pair(self, seq1: PValueSequence, p_values1: list, seq2: PValueSequence, p_values2: list):
        pair = (seq1, seq2)
        if pair in self._pairs:
            raise ValueError('Pair of given sequences already exists')
        if seq1 == seq2:
            raise ValueError('seq1 and seq2 are the same')
        self._pairs[(seq1, seq2)] = (p_values1, p_values2)

    def get_p_values_for_sequences(self, seq1: PValueSequence, seq2: PValueSequence):
        pair = (seq1, seq2)
        ret = self._pairs.get(pair, None)
        if ret is None:
            raise ValueError('p-values for given sequences do not exist')
        return ret
