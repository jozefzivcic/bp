from unittest import TestCase

from nist_statistics.line_generator import LineGenerator
from nist_statistics.test_statistics import TestStatistics


class TestLineGenerator(TestCase):
    def setUp(self):
        self.line_generator = LineGenerator()

    def test_basics(self):
        test_stat = TestStatistics()
        test_stat.p_value_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        test_stat.total_tested = 55
        test_stat.total_passed = 40
        expected_output = '  1   2   3   4   5   6   7   8   9  10' \
                          '  0.000000     40/55'
        output = self.line_generator.generate_line_from_test_statistics(test_stat)
        self.assertEqual(output, expected_output, '\n             Output: ' + output + '\nand expected output: ' +
                         expected_output +'\nare not the same')