from unittest import TestCase

from nist_statistics.line_generator import LineGenerator
from nist_statistics.test_statistics_dto import TestStatisticsDTO

p_values_str = '  1   2   3   4   5   6   7   8   9  10'


def fnc_assert_output(tester, output, expected_output):
    tester.assertEqual(output, expected_output, '\n             Output: ' + output + '\nand expected output: ' +
                       expected_output + '\nare not the same')


class TestLineGenerator(TestCase):
    def setUp(self):
        self.line_generator = LineGenerator()
        self.test_stat = TestStatisticsDTO()
        self.test_stat.p_value_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.test_stat.total_tested = 55
        self.test_stat.total_passed = 40
        self.test_stat.p_value = 0.5
        self.test_stat.test_name = 'Frequency'

    def test_units_of_seq(self):
        self.test_stat.total_passed = 5
        self.test_stat.total_tested = 9
        expected_output = p_values_str + '  0.500000      5/9       Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_tens_of_seq(self):
        expected_output = p_values_str + '  0.500000     40/55      Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_hundreds_of_seq(self):
        self.test_stat.total_passed = 500
        self.test_stat.total_tested = 687
        expected_output = p_values_str + '  0.500000    500/687     Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_thousands_of_seq(self):
        self.test_stat.total_passed = 5000
        self.test_stat.total_tested = 6874
        expected_output = p_values_str + '  0.500000   5000/6874    Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_ten_thousands_of_seq(self):
        self.test_stat.total_passed = 50000
        self.test_stat.total_tested = 68743
        expected_output = p_values_str + '  0.500000  50000/68743   Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_hundred_thousand_of_seq(self):
        self.test_stat.total_passed = 500000
        self.test_stat.total_tested = 100000
        expected_output = p_values_str + '  0.500000 500000/100000  Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_million_of_seq(self):
        self.test_stat.total_passed = 5000000
        self.test_stat.total_tested = 1000000
        expected_output = p_values_str + '  0.500000 5000000/1000000 Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_ten_millions_of_seq(self):
        self.test_stat.total_passed = 50000000
        self.test_stat.total_tested = 10000000
        expected_output = p_values_str + '  0.500000 50000000/10000000 Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    # Testing of zero p-value

    def test_units_of_seq_zero_p_value(self):
        self.test_stat.p_value = 0.0
        self.test_stat.total_passed = 5
        self.test_stat.total_tested = 9
        expected_output = p_values_str + '  0.000000 *    5/9 *     Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_tens_of_seq_zero_p_value(self):
        self.test_stat.p_value = 0.0
        expected_output = p_values_str + '  0.000000 *   40/55 *    Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_hundreds_of_seq_zero_p_value(self):
        self.test_stat.p_value = 0.0
        self.test_stat.total_passed = 500
        self.test_stat.total_tested = 687
        expected_output = p_values_str + '  0.000000 *  500/687 *   Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_thousands_of_seq_zero_p_value(self):
        self.test_stat.p_value = 0.0
        self.test_stat.total_passed = 5000
        self.test_stat.total_tested = 6874
        expected_output = p_values_str + '  0.000000 * 5000/6874 *  Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_ten_thousands_of_seq_zero_p_value(self):
        self.test_stat.p_value = 0.0
        self.test_stat.total_passed = 50000
        self.test_stat.total_tested = 68743
        expected_output = p_values_str + '  0.000000 * 50000/68743 * Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_hundred_thousand_of_seq_zero_p_value(self):
        self.test_stat.p_value = 0.0
        self.test_stat.total_passed = 500000
        self.test_stat.total_tested = 100000
        expected_output = p_values_str + '  0.000000 * 500000/100000 * Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_million_of_seq_zero_p_value(self):
        self.test_stat.p_value = 0.0
        self.test_stat.total_passed = 5000000
        self.test_stat.total_tested = 1000000
        expected_output = p_values_str + '  0.000000 * 5000000/1000000 * Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_ten_millions_of_seq_zero_p_value(self):
        self.test_stat.p_value = 0.0
        self.test_stat.total_passed = 50000000
        self.test_stat.total_tested = 10000000
        expected_output = p_values_str + '  0.000000 * 50000000/10000000 * Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)
