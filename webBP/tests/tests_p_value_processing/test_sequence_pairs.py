from unittest import TestCase

from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_pairs import SequencePairs
from tests.data_for_tests.common_data import TestsIdData, dict_for_test_13, dict_for_test_14, dict_for_test_41, \
    dict_for_test_42


class TestSequencePairs(TestCase):
    def setUp(self):
        self.seq_pairs = SequencePairs()

    def test_add_pair(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)
        p_values1 = dict_for_test_13['results']
        p_values2 = dict_for_test_14['data1']

        seq3 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 1)
        seq4 = PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS)
        p_values3 = dict_for_test_41['data1']
        p_values4 = dict_for_test_42['results']

        self.seq_pairs.add_pair(seq1, p_values1, seq2, p_values2)
        self.seq_pairs.add_pair(seq3, p_values3, seq4, p_values4)

        ret1, ret2 = self.seq_pairs.get_p_values_for_sequences(seq1, seq2)
        self.assertEqual(p_values1, ret1)
        self.assertEqual(p_values2, ret2)

        ret3, ret4 = self.seq_pairs.get_p_values_for_sequences(seq3, seq4)
        self.assertEqual(p_values3, ret3)
        self.assertEqual(p_values4, ret4)
