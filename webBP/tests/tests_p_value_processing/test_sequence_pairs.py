from unittest import TestCase

from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_pairs import SequencePairs
from tests.data_for_tests.common_data import TestsIdData, dict_for_test_13, dict_for_test_14, dict_for_test_41, \
    dict_for_test_42, dict_for_test_43


class TestSequencePairs(TestCase):
    def add_all_pairs(self):
        self.seq_pairs.add_pair(self.seq1, self.p_values1, self.seq2, self.p_values2)
        self.seq_pairs.add_pair(self.seq1, self.p_values1, self.seq3, self.p_values3)
        self.seq_pairs.add_pair(self.seq1, self.p_values1, self.seq4, self.p_values4)
        self.seq_pairs.add_pair(self.seq1, self.p_values1, self.seq5, self.p_values5)

        self.seq_pairs.add_pair(self.seq2, self.p_values2, self.seq3, self.p_values3)
        self.seq_pairs.add_pair(self.seq2, self.p_values2, self.seq4, self.p_values4)
        self.seq_pairs.add_pair(self.seq2, self.p_values2, self.seq5, self.p_values5)

        self.seq_pairs.add_pair(self.seq3, self.p_values3, self.seq4, self.p_values4)
        self.seq_pairs.add_pair(self.seq3, self.p_values3, self.seq5, self.p_values5)

        self.seq_pairs.add_pair(self.seq4, self.p_values4, self.seq5, self.p_values5)

    def setUp(self):
        self.seq_pairs = SequencePairs()

        self.seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        self.seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)
        self.seq3 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)
        self.seq4 = PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS)
        self.seq5 = PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS)

        self.p_values1 = dict_for_test_13['results']
        self.p_values2 = dict_for_test_14['data1']
        self.p_values3 = dict_for_test_41['data2']
        self.p_values4 = dict_for_test_42['results']
        self.p_values5 = dict_for_test_43['results']

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

    def test_add_existing_pair(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)

        p_values1 = dict_for_test_13['results']
        p_values2 = dict_for_test_14['data1']
        p_values3 = dict_for_test_42['results']
        p_values4 = dict_for_test_41['data1']

        self.seq_pairs.add_pair(seq1, p_values1, seq2, p_values2)

        with self.assertRaises(ValueError) as context:
            self.seq_pairs.add_pair(seq1, p_values1, seq2, p_values2)
        self.assertEqual('Pair of given sequences already exists', str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.seq_pairs.add_pair(seq1, p_values3, seq2, p_values4)
        self.assertEqual('Pair of given sequences already exists', str(context.exception))

    def test_add_pair_same_sequences(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        p_values1 = dict_for_test_13['results']
        p_values2 = dict_for_test_14['data1']
        with self.assertRaises(ValueError) as context:
            self.seq_pairs.add_pair(seq1, p_values1, seq1, p_values2)
        self.assertEqual('seq1 and seq2 are the same', str(context.exception))

    def test_get_p_values_for_sequences_non_existing_sequence_pair(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)
        seq3 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 1)
        seq4 = PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS)

        p_values1 = dict_for_test_13['results']
        p_values2 = dict_for_test_14['data1']

        with self.assertRaises(ValueError) as context:
            self.seq_pairs.get_p_values_for_sequences(seq1, seq2)
        self.assertEqual('p-values for given sequences do not exist', str(context.exception))

        self.seq_pairs.add_pair(seq1, p_values1, seq2, p_values2)

        with self.assertRaises(ValueError) as context:
            self.seq_pairs.get_p_values_for_sequences(seq2, seq1)
        self.assertEqual('p-values for given sequences do not exist', str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.seq_pairs.get_p_values_for_sequences(seq3, seq4)
        self.assertEqual('p-values for given sequences do not exist', str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.seq_pairs.get_p_values_for_sequences(seq4, seq3)
        self.assertEqual('p-values for given sequences do not exist', str(context.exception))

    def test_get_pairs_in_list(self):
        self.add_all_pairs()

        seq_pairs_list = self.seq_pairs.get_pairs_in_list()

        self.cmp_tuples((self.seq1, self.seq2, self.p_values1, self.p_values2), seq_pairs_list[0])
        self.cmp_tuples((self.seq1, self.seq3, self.p_values1, self.p_values3), seq_pairs_list[1])
        self.cmp_tuples((self.seq1, self.seq4, self.p_values1, self.p_values4), seq_pairs_list[2])
        self.cmp_tuples((self.seq1, self.seq5, self.p_values1, self.p_values5), seq_pairs_list[3])

        self.cmp_tuples((self.seq2, self.seq3, self.p_values2, self.p_values3), seq_pairs_list[4])
        self.cmp_tuples((self.seq2, self.seq4, self.p_values2, self.p_values4), seq_pairs_list[5])
        self.cmp_tuples((self.seq2, self.seq5, self.p_values2, self.p_values5), seq_pairs_list[6])

        self.cmp_tuples((self.seq3, self.seq4, self.p_values3, self.p_values4), seq_pairs_list[7])
        self.cmp_tuples((self.seq3, self.seq5, self.p_values3, self.p_values5), seq_pairs_list[8])

        self.cmp_tuples((self.seq4, self.seq5, self.p_values4, self.p_values5), seq_pairs_list[9])

    def test_filter_pairs(self):
        def filter_func(values1: list, values2: list):
            if len(values1) != len(values2):
                raise ValueError('Lengths are not the same')
            if values1[0] < 0.5 or values2[0] < 0.5:
                return True
            return False

        self.add_all_pairs()

        self.seq_pairs.filter_pairs(filter_func)
        seq_pairs_list = self.seq_pairs.get_pairs_in_list()
        self.assertEqual(3, len(seq_pairs_list))

        self.cmp_tuples((self.seq1, self.seq2, self.p_values1, self.p_values2), seq_pairs_list[0])
        self.cmp_tuples((self.seq1, self.seq3, self.p_values1, self.p_values3), seq_pairs_list[1])
        self.cmp_tuples((self.seq2, self.seq3, self.p_values2, self.p_values3), seq_pairs_list[2])

    def test_filter_out_all_pairs(self):
        self.add_all_pairs()
        seq_pairs_list = self.seq_pairs.get_pairs_in_list()
        self.assertEqual(10, len(seq_pairs_list))

        self.seq_pairs.filter_pairs(lambda x, y: False)
        seq_pairs_list = self.seq_pairs.get_pairs_in_list()
        self.assertEqual(10, len(seq_pairs_list))

        self.seq_pairs.filter_pairs(lambda x, y: True)
        seq_pairs_list = self.seq_pairs.get_pairs_in_list()
        self.assertEqual(0, len(seq_pairs_list))

    def cmp_tuples(self, expected, ret):
        for i in range(4):
            self.assertEqual(expected[i], ret[i], 'Expected ' + str(expected[i]) + ', but ' + str(ret[i]) + ' was given.')
