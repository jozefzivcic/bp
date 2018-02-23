from unittest import TestCase

from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType


class TestDataSourceInfo(TestCase):
    def setUp(self):
        self.p_value_seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        self.p_value_seq2 = PValueSequence(1, PValuesFileType.DATA, 2)

    def get_error_message(self, tests_in_chart, p_value_sequence):
        return 'Arguments tests_in_chart: {} and p_value_sequence {} are not alowed' \
            .format(tests_in_chart, str(type(p_value_sequence)))

    def test_constructor_wrong_p_value_seq_type_with_single_test(self):
        with self.assertRaises(ValueError) as ex:
            DataSourceInfo(TestsInChart.SINGLE_TEST, [])
        self.assertEqual(self.get_error_message(TestsInChart.SINGLE_TEST, []), str(ex.exception))

    def test_constructor_wrong_p_value_seq_type_with_pair_of_tests(self):
        with self.assertRaises(ValueError) as ex:
            DataSourceInfo(TestsInChart.PAIR_OF_TESTS, [])
        self.assertEqual(self.get_error_message(TestsInChart.PAIR_OF_TESTS, []), str(ex.exception))

    def test_constructor_tuple_wrong_length_with_pair_of_tests(self):
        with self.assertRaises(ValueError) as ex:
            DataSourceInfo(TestsInChart.PAIR_OF_TESTS, ())
        self.assertEqual('Tuple should contain exactly two PValueSequence objects for TestsInChart.PAIR_OF_TESTS',
                         str(ex.exception))

    def test_constructor_wrong_p_value_seq_type_with_multiple_tests(self):
        with self.assertRaises(ValueError) as ex:
            DataSourceInfo(TestsInChart.MULTIPLE_TESTS, (self.p_value_seq1, ))
        self.assertEqual(self.get_error_message(TestsInChart.MULTIPLE_TESTS, (self.p_value_seq1, )), str(ex.exception))

    def test_constructor_list_wrong_length_multiple_tests(self):
        with self.assertRaises(ValueError) as ex:
            DataSourceInfo(TestsInChart.MULTIPLE_TESTS, [])
        self.assertEqual('Multiple tests cannot have empty list', str(ex.exception))

    def test_are_equal(self):
        d1 = DataSourceInfo(TestsInChart.SINGLE_TEST, self.p_value_seq1)
        d2 = DataSourceInfo(TestsInChart.SINGLE_TEST, self.p_value_seq1)
        self.assertEqual(d1, d2)

        d1 = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (self.p_value_seq1, self.p_value_seq2))
        d2 = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (self.p_value_seq1, self.p_value_seq2))
        self.assertEqual(d1, d2)

        d1 = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, [self.p_value_seq1])
        d2 = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, [self.p_value_seq1])
        self.assertEqual(d1, d2)

    def test_are_not_equal_different_tests_in_chart(self):
        d1 = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (self.p_value_seq1, self.p_value_seq2))
        d2 = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, [self.p_value_seq1])
        self.assertNotEqual(d1, d2)

    def test_are_not_equal_different_tests_seq(self):
        d1 = DataSourceInfo(TestsInChart.SINGLE_TEST, self.p_value_seq1)
        d2 = DataSourceInfo(TestsInChart.SINGLE_TEST, self.p_value_seq2)
        self.assertNotEqual(d1, d2)

    def test_are_not_equal_different_object(self):
        d1 = DataSourceInfo(TestsInChart.SINGLE_TEST, self.p_value_seq1)
        self.assertNotEqual(d1, 4)

