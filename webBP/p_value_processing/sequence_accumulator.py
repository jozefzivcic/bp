import itertools

from enums.test_dep_pairs import TestDepPairs
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_pairs import SequencePairs


class SequenceAccumulator:
    def __init__(self):
        self._seq = {}

    def add_sequence(self, seq: PValueSequence):
        if seq.test_id in self._seq:
            self._seq[seq.test_id].append(seq)
        else:
            self._seq[seq.test_id] = [seq]

    def get_all_sequences(self):
        ret = []
        for key, value in self._seq.items():
            ret.extend(value)
        return ret

    def generate_sequence_pairs(self, acc: PValuesAccumulator, pairs: TestDepPairs=TestDepPairs.ALL_PAIRS) \
            -> SequencePairs:
        seq_pairs = SequencePairs()
        sequences = self.filter_sequences(acc.get_all_test_ids())
        combinations = itertools.combinations(sequences, 2)
        for seq1, seq2 in combinations:
            if pairs == TestDepPairs.SKIP_PAIRS_FROM_SUBTESTS and self.is_sub_test(seq1, seq2):
                continue
            p_values1 = self.get_p_values_for_sequence(seq1, acc)
            p_values2 = self.get_p_values_for_sequence(seq2, acc)
            seq_pairs.add_pair(seq1, p_values1, seq2, p_values2)
        return seq_pairs

    def get_p_values_for_sequence(self, sequence: PValueSequence, acc: PValuesAccumulator) -> list:
        dto = acc.get_dto_for_test(sequence.test_id)
        if sequence.p_values_file == PValuesFileType.RESULTS:
            return dto.get_results_p_values()
        else:
            return dto.get_data_p_values(sequence.data_num)

    def filter_sequences(self, test_id_list: list):
        sequences = []
        for test_id in test_id_list:
            temp_seq = self._seq.get(test_id, None)
            if temp_seq is None:
                continue
            sequences.extend(temp_seq)
        return sequences

    def is_sub_test(self, seq1: PValueSequence, seq2: PValueSequence) -> bool:
        return seq1.test_id == seq2.test_id

