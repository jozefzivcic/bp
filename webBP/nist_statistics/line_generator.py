from nist_statistics.test_statistics import TestStatistics


class LineGenerator:
    def generate_line_from_test_statistics(self, test_stat_obj: TestStatistics) -> str:
        output = ''
        for num in test_stat_obj.p_value_array:
            output += '%3d ' % num
        output += ' %8.6f' % 0.0
        output += '     '
        output += str(test_stat_obj.total_passed)
        output += '/'
        output += str(test_stat_obj.total_tested)
        return output