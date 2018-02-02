from unittest import TestCase

from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_accumulator import SequenceAccumulator
from tests.data_for_tests.common_data import TestsIdData, dict_for_test_13, dict_for_test_14, dict_for_test_41, \
    dict_for_test_42, dict_for_test_43


class TestSequenceAccumulator(TestCase):
    def setUp(self):
        self.seq_acc = SequenceAccumulator()

        self.p_values_dto_for_test1 = PValuesDto(dict_for_test_13)
        self.p_values_dto_for_test2 = PValuesDto(dict_for_test_14)
        self.p_values_dto_for_test3 = PValuesDto(dict_for_test_41)
        self.p_values_dto_for_test4 = PValuesDto(dict_for_test_42)
        self.p_values_dto_for_test5 = PValuesDto(dict_for_test_43)

        self.p_values_acc = PValuesAccumulator()
        self.p_values_acc.add(TestsIdData.test1_id, self.p_values_dto_for_test1)
        self.p_values_acc.add(TestsIdData.test2_id, self.p_values_dto_for_test2)
        self.p_values_acc.add(TestsIdData.test3_id, self.p_values_dto_for_test3)
        self.p_values_acc.add(TestsIdData.test4_id, self.p_values_dto_for_test4)
        self.p_values_acc.add(TestsIdData.test5_id, self.p_values_dto_for_test5)

    def test_add_sequence(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        self.seq_acc.add_sequence(seq1)

        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 4)
        self.seq_acc.add_sequence(seq2)

        ret = self.seq_acc.get_all_sequences()

        self.assertEqual(2, len(ret))

        expected = list(filter(lambda x: x.test_id == TestsIdData.test1_id, ret))[0]
        self.assertEqual(seq1.p_values_file, expected.p_values_file)
        self.assertIsNone(expected.data_num)

        expected = list(filter(lambda x: x.test_id == TestsIdData.test2_id, ret))[0]
        self.assertEqual(seq2.p_values_file, expected.p_values_file)
        self.assertEqual(seq2.data_num, expected.data_num)

    def test_generate_sequence_pairs_no_sequence_empty_p_values_acc(self):
        p_values_acc = PValuesAccumulator()
        seq_pairs = self.seq_acc.generate_sequence_pairs(p_values_acc)
        pairs = seq_pairs.get_pairs_in_list()
        self.assertEqual(0, len(pairs))

    def test_generate_sequence_pairs_no_sequence(self):
        seq_pairs = self.seq_acc.generate_sequence_pairs(self.p_values_acc)
        pairs = seq_pairs.get_pairs_in_list()
        self.assertEqual(0, len(pairs))

    def test_generate_sequence_pairs_one_sequence_empty_p_values_acc(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        self.seq_acc.add_sequence(seq1)

        p_values_acc = PValuesAccumulator()
        seq_pairs = self.seq_acc.generate_sequence_pairs(p_values_acc)
        pairs = seq_pairs.get_pairs_in_list()
        self.assertEqual(0, len(pairs))

    def test_generate_sequence_pairs_one_sequence(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        self.seq_acc.add_sequence(seq1)

        seq_pairs = self.seq_acc.generate_sequence_pairs(self.p_values_acc)
        pairs = seq_pairs.get_pairs_in_list()
        self.assertEqual(0, len(pairs))

    def test_generate_sequence_pairs_two_sequences_smallest_p_values_acc(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)
        self.seq_acc.add_sequence(seq1)
        self.seq_acc.add_sequence(seq2)

        p_values_acc = PValuesAccumulator()
        p_values_acc.add(TestsIdData.test1_id, self.p_values_dto_for_test1)
        p_values_acc.add(TestsIdData.test2_id, self.p_values_dto_for_test2)

        seq_pairs = self.seq_acc.generate_sequence_pairs(p_values_acc)

        seq_pairs_list = seq_pairs.get_pairs_in_list()
        self.assertEqual(1, len(seq_pairs_list))

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq1, seq2)
        self.assertEqual(dict_for_test_13['results'], values1)
        self.assertEqual(dict_for_test_14['data1'], values2)

    def test_generate_sequence_pairs_two_sequences(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)
        self.seq_acc.add_sequence(seq1)
        self.seq_acc.add_sequence(seq2)

        seq_pairs = self.seq_acc.generate_sequence_pairs(self.p_values_acc)

        seq_pairs_list = seq_pairs.get_pairs_in_list()
        self.assertEqual(1, len(seq_pairs_list))

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq1, seq2)
        self.assertEqual(dict_for_test_13['results'], values1)
        self.assertEqual(dict_for_test_14['data1'], values2)

    def test_generate_sequence_pairs_more_sequences(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)
        seq3 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)
        seq4 = PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS)
        seq5 = PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS)

        self.seq_acc.add_sequence(seq1)
        self.seq_acc.add_sequence(seq2)
        self.seq_acc.add_sequence(seq3)
        self.seq_acc.add_sequence(seq4)
        self.seq_acc.add_sequence(seq5)

        seq_pairs = self.seq_acc.generate_sequence_pairs(self.p_values_acc)

        self.assertEqual(10, len(seq_pairs._pairs))

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq1, seq2)
        self.assertEqual(dict_for_test_13['results'], values1)
        self.assertEqual(dict_for_test_14['data1'], values2)

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq1, seq3)
        self.assertEqual(dict_for_test_13['results'], values1)
        self.assertEqual(dict_for_test_41['data2'], values2)

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq1, seq4)
        self.assertEqual(dict_for_test_13['results'], values1)
        self.assertEqual(dict_for_test_42['results'], values2)

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq1, seq5)
        self.assertEqual(dict_for_test_13['results'], values1)
        self.assertEqual(dict_for_test_43['results'], values2)

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq2, seq3)
        self.assertEqual(dict_for_test_14['data1'], values1)
        self.assertEqual(dict_for_test_41['data2'], values2)

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq2, seq4)
        self.assertEqual(dict_for_test_14['data1'], values1)
        self.assertEqual(dict_for_test_42['results'], values2)

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq2, seq5)
        self.assertEqual(dict_for_test_14['data1'], values1)
        self.assertEqual(dict_for_test_43['results'], values2)

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq3, seq4)
        self.assertEqual(dict_for_test_41['data2'], values1)
        self.assertEqual(dict_for_test_42['results'], values2)

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq3, seq5)
        self.assertEqual(dict_for_test_41['data2'], values1)
        self.assertEqual(dict_for_test_43['results'], values2)

        values1, values2 = seq_pairs.get_p_values_for_sequences(seq4, seq5)
        self.assertEqual(dict_for_test_42['results'], values1)
        self.assertEqual(dict_for_test_43['results'], values2)

    def test_get_p_values_for_sequence_from_results_file(self):
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        expected = dict_for_test_13['results']
        ret = self.seq_acc.get_p_values_for_sequence(seq, self.p_values_acc)
        self.assertEqual(expected, ret)

    def test_get_p_values_for_sequence_from_data_1_file(self):
        seq = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)
        expected = dict_for_test_14['data1']
        ret = self.seq_acc.get_p_values_for_sequence(seq, self.p_values_acc)
        self.assertEqual(expected, ret)

    def test_get_p_values_for_sequence_from_data_2_file(self):
        seq = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        expected = dict_for_test_14['data2']
        ret = self.seq_acc.get_p_values_for_sequence(seq, self.p_values_acc)
        self.assertEqual(expected, ret)

    def test_get_p_values_for_sequence_from_non_existing_data_file(self):
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.DATA, 2)
        with self.assertRaises(ValueError) as context:
            self.seq_acc.get_p_values_for_sequence(seq, self.p_values_acc)

    def test_get_p_values_for_sequence_from_non_existing_test_id(self):
        seq = PValueSequence(TestsIdData.non_existing_test_id, PValuesFileType.RESULTS)
        with self.assertRaises(ValueError) as context:
            self.seq_acc.get_p_values_for_sequence(seq, self.p_values_acc)
