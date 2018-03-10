from common.unif_check import UnifCheck
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

    def filter_pairs(self, check_obj: UnifCheck, remove_non_uniform=False):
        """
        Filter pairs stored in this object according to func.
        :param check_obj: UnifCheck object. Based on this object, pairs are filtered out and info about approximation
        condition fulfilling is gained. This object decides, whether points in 2D space are equally distributed.
        :param remove_non_uniform: If True, pairs whose distribution looks to be non-uniform, will be removed. Only
        pairs, whose distribution looks to be uniform, will not be removed. For False, vice-versa.
        """
        to_keep = []
        to_delete = []
        for key, value in self._pairs.items():
            seq1 = value[0]
            seq2 = value[1]
            if self.should_remove(check_obj, seq1, seq2, remove_non_uniform):
                condition = check_obj.is_approx_fulfilled()
                to_delete.append((key, condition))
            else:
                condition = check_obj.is_approx_fulfilled()
                to_keep.append()
        for key in to_delete:
            del self._pairs[key]

    def should_remove(self, check_obj: UnifCheck, seq1: list, seq2: list, remove_non_uniform) -> tuple:
        """
        Decides, whether to remove or not pair of sequences based on the object.
        :param check_obj: UnifCheck object.
        :param seq1: First list of p-values.
        :param seq2: Second list of p-values.
        :param remove_non_uniform: If True, pairs whose distribution looks to be non-uniform, will be removed. Only
        pairs, whose distribution looks to be uniform, will not be removed. For False, vice-versa.
        :return: Tuple. First element denotes whether to remove given pair of sequences. It is True, if given sequences
        should be removed. False otherwise. The second element denotes, whether the condition of good approximation was
        fulfilled.
        """
        hypothesis_rejected = check_obj.check_for_uniformity(seq1, seq2)
        is_condition_fulfilled = check_obj.is_approx_fulfilled()
        if remove_non_uniform:
            return hypothesis_rejected, is_condition_fulfilled
        else:
            return not hypothesis_rejected, is_condition_fulfilled
