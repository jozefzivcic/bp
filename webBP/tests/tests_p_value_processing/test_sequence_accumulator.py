from unittest import TestCase

from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_accumulator import SequenceAccumulator
from tests.data_for_tests.common_data import TestsIdData


class TestSequenceAccumulator(TestCase):
    def setUp(self):
        self.seq_acc = SequenceAccumulator()

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
