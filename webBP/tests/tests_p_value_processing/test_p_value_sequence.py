from unittest import TestCase

from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType


class TestPValueSequence(TestCase):
    def test_data_num_not_none(self):
        with self.assertRaises(ValueError) as context:
            seq = PValueSequence(4, PValuesFileType.RESULTS, 1)
        self.assertEqual('data_num is not None, when using RESULTS file type', str(context.exception))

    def test_data_num_none(self):
        with self.assertRaises(ValueError) as context:
            seq = PValueSequence(4, PValuesFileType.DATA)
        self.assertEqual('unspecified number of data file', str(context.exception))

    def test_data_num_not_int(self):
        with self.assertRaises(TypeError) as context:
            seq = PValueSequence(4, PValuesFileType.DATA, '456')
        self.assertEqual('data_num has a wrong type <class \'str\'>', str(context.exception))

    def test_eq_none(self):
        seq = PValueSequence(4, PValuesFileType.RESULTS)
        self.assertFalse(seq == None)
        self.assertTrue(seq != None)

    def test_eq_other_object(self):
        seq = PValueSequence(4, PValuesFileType.RESULTS)
        self.assertFalse(seq == {})
        self.assertTrue(seq != {})

    def test_eq_test_ids_differ(self):
        seq1 = PValueSequence(3, PValuesFileType.RESULTS)
        seq2 = PValueSequence(4, PValuesFileType.RESULTS)
        self.assertFalse(seq1 == seq2)
        self.assertTrue(seq1 != seq2)

        seq1 = PValueSequence(3, PValuesFileType.DATA, 1)
        seq2 = PValueSequence(4, PValuesFileType.DATA, 1)
        self.assertFalse(seq1 == seq2)
        self.assertTrue(seq1 != seq2)

    def test_eq_file_types_differ(self):
        seq1 = PValueSequence(3, PValuesFileType.RESULTS)
        seq1.data_num = 4
        seq2 = PValueSequence(3, PValuesFileType.DATA, 4)

        self.assertFalse(seq1 == seq2)
        self.assertTrue(seq1 != seq2)

    def test_eq_data_num_differ(self):
        seq1 = PValueSequence(3, PValuesFileType.DATA, 1)
        seq2 = PValueSequence(3, PValuesFileType.DATA, 12)

        self.assertFalse(seq1 == seq2)
        self.assertTrue(seq1 != seq2)

    def test_eq_are_equal(self):
        seq1 = PValueSequence(4, PValuesFileType.RESULTS)
        seq2 = PValueSequence(4, PValuesFileType.RESULTS)

        self.assertTrue(seq1 == seq2)
        self.assertFalse(seq1 != seq2)

        seq1 = PValueSequence(4, PValuesFileType.DATA, 1)
        seq2 = PValueSequence(4, PValuesFileType.DATA, 1)

        self.assertTrue(seq1 == seq2)
        self.assertFalse(seq1 != seq2)
