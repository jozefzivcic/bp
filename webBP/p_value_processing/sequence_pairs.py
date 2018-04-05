from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart
from common.unif_check import UnifCheck
from enums.filter_uniformity import FilterUniformity
from p_value_processing.data_from_filter_pairs import DataFromFilterPairs
from p_value_processing.different_lists_size_error import DifferentListsSizeError
from p_value_processing.filtered_item_dto import FilteredItemDto
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
        ret.sort(key=lambda pair: (pair[0], pair[1]))
        return ret

    def filter_pairs(self, check_obj: UnifCheck, filter_unif: FilterUniformity) -> DataFromFilterPairs:
        """
        Filter pairs stored in this object according to func.
        :param check_obj: UnifCheck object. Based on this object, pairs are filtered out and info about approximation
        condition fulfilling is gained. This object decides, whether points in 2D space are equally distributed.
        :param filter_unif: If True, pairs whose distribution looks to be non-uniform, will be removed. Only
        pairs, whose distribution looks to be uniform, will not be removed. For False, vice-versa.
        """
        to_delete = []
        data_from_fp = DataFromFilterPairs()
        for key, value in self._pairs.items():
            seq1 = value[0]
            seq2 = value[1]

            try:
                should_remove, p_value, condition = self.should_remove(check_obj, seq1, seq2, filter_unif)
            except RuntimeError as ex:
                raise DifferentListsSizeError(str(ex), key[0], len(seq1), key[1], len(seq2))
            ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, key)
            item = FilteredItemDto(ds_info, p_value, condition)

            if should_remove:
                to_delete.append(key)
                data_from_fp.add_deleted(item)
            else:
                data_from_fp.add_kept(item)
        for key in to_delete:
            del self._pairs[key]
        return data_from_fp

    def should_remove(self, check_obj: UnifCheck, seq1: list, seq2: list, filter_unif: FilterUniformity) -> tuple:
        """
        Decides, whether to remove or not pair of sequences based on the object.
        :param check_obj: UnifCheck object.
        :param seq1: First list of p-values.
        :param seq2: Second list of p-values.
        :param filter_unif: If True, pairs whose distribution looks to be non-uniform, will be removed. Only
        pairs, whose distribution looks to be uniform, will not be removed. For False, vice-versa.
        :return: Tuple. First element denotes whether to remove given pair of sequences. It is True, if given sequences
        should be removed. False otherwise. The second element denotes p-value from uniformity check test.
        The last element denotes, whether the condition of good approximation was fulfilled.
        """
        hypothesis_rejected = check_obj.check_for_uniformity(seq1, seq2)
        p_value = check_obj.get_p_value()
        is_condition_fulfilled = check_obj.is_approx_fulfilled()
        if filter_unif == FilterUniformity.REMOVE_NON_UNIFORM:
            return hypothesis_rejected, p_value, is_condition_fulfilled
        elif filter_unif == FilterUniformity.REMOVE_UNIFORM:
            return not hypothesis_rejected, p_value, is_condition_fulfilled
        elif filter_unif == FilterUniformity.DO_NOT_FILTER:
            return False, p_value, is_condition_fulfilled
        else:
            raise ValueError('Unknown type of FilterUniformity: {}'.format(filter_unif))
