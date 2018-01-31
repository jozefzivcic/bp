import itertools

from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_pairs import SequencePairs


class SequenceAccumulator:
    def __init__(self):
        self._seq = []

    def add_sequence(self, seq: PValueSequence):
        self._seq.append(seq)

    def get_all_sequences(self):
        return list(self._seq)

    def generate_sequence_pairs(self, acc: PValuesAccumulator) -> SequencePairs:
        seq_pairs = SequencePairs()
        combinations = itertools.combinations(self._seq, 2)
        for seq1, seq2 in combinations:
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
