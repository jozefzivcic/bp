from unittest import TestCase

from nist_statistics.line_generator import LineGenerator
from nist_statistics.test_statistics_dto import TestStatisticsDTO

p_values_str = '  1   2   3   4   5   6   7   8   9  10 '


def fnc_assert_output(tester, output, expected_output):
    tester.assertEqual(output, expected_output, '\n             Output: ' + output + '\nand expected output: ' +
                       expected_output + '\nare not the same')


class TestLineGenerator(TestCase):
    def setUp(self):
        self.line_generator = LineGenerator()
        self.test_stat = TestStatisticsDTO()
        self.test_stat.p_value_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.test_stat.test_name = 'Frequency'

    def test_all_dashes(self):
        expected_output = p_values_str + '    ----    ' + '    ----    ' + ' ----     ' + 'Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_small_uniformity_pvalue(self):
        self.test_stat.exp_count = 1
        self.test_stat.uniformity_p_value = 0.00009
        expected_output = p_values_str + ' 0.000090 * ' + ' 0.000000 * ' + ' ----     ' + 'Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_large_uniformity_pvalue(self):
        self.test_stat.exp_count = 1
        self.test_stat.uniformity_p_value = 0.7894
        expected_output = p_values_str + ' 0.789400   ' + ' 0.000000 * ' + ' ----     ' + 'Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_small_KS_pvalue(self):
        self.test_stat.exp_count = 1
        self.test_stat.KS_p_value = 0.00004
        expected_output = p_values_str + ' 0.000000 * ' + ' 0.000040 * ' + ' ----     ' + 'Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_large_KS_pvalue(self):
        self.test_stat.exp_count = 1
        self.test_stat.KS_p_value = 0.456
        expected_output = p_values_str + ' 0.000000 * ' + ' 0.456000   ' + ' ----     ' + 'Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_proportion_less_than_threshold(self):
        self.test_stat.sample_size = 1
        self.test_stat.proportion = 0.5
        self.test_stat.proportion_threshold_min  = 0.51
        self.test_stat.proportion_threshold_max = 0.6
        expected_output = p_values_str + '    ----    ' + '    ----    ' + '0.5000 *  ' + 'Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_proportion_more_than_threshold(self):
        self.test_stat.sample_size = 1
        self.test_stat.proportion = 0.5
        self.test_stat.proportion_threshold_min  = 0.4
        self.test_stat.proportion_threshold_max = 0.49
        expected_output = p_values_str + '    ----    ' + '    ----    ' + '0.5000 *  ' + 'Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)

    def test_proportion_between_thresholds(self):
        self.test_stat.sample_size = 1
        self.test_stat.proportion = 0.5
        self.test_stat.proportion_threshold_min = 0.49
        self.test_stat.proportion_threshold_max = 0.51
        expected_output = p_values_str + '    ----    ' + '    ----    ' + '0.5000    ' + 'Frequency'
        output = self.line_generator.generate_line_from_test_statistics(self.test_stat)
        fnc_assert_output(self, output, expected_output)
