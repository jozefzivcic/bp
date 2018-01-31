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

    def get_pairs_in_list(self):
        ret = []
        for key, value in self._pairs.items():
            ret.append(key + value)
        ret.sort(key=lambda pair: (pair[0].test_id, pair[1].test_id))
        return ret

    def filter_pairs(self, func):
        """
        Filter pairs stored in this object according to func.
        :param func: Function, which takes two lists of p_values as arguments and returns False if the pair
        corresponding to the two lists given as argument should not be erased. If this function returns True,
        the corresponding pair will be erased from this object.
        """
        to_delete = []
        for key, value in self._pairs.items():
            seq1 = value[0]
            seq2 = value[1]
            if func(seq1, seq2):
                to_delete.append(key)
        for key in to_delete:
            del self._pairs[key]
