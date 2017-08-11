from nist_statistics.test_statistics_dto import TestStatisticsDTO


class LineGenerator:
    def generate_line_from_test_statistics(self, test_stat_obj: TestStatisticsDTO) -> str:
        output = ''
        for num in test_stat_obj.p_value_array:
            output += '%3d ' % num
        # TODO: ---- if p-value should not be presented
        output += ' %8.6f' % test_stat_obj.p_value
        if test_stat_obj.p_value > 0.0000001:
            output += ' '
            output += '%6d' % test_stat_obj.total_passed
        else:
            output += ' * '
            output += '%4d' % test_stat_obj.total_passed
        output += '/'
        output += str(test_stat_obj.total_tested)
        if test_stat_obj.p_value > 0.0000001:
            output += ' ' + ' ' * (7 - len(str(test_stat_obj.total_tested)))
        else:
            output += (' * ' + ' ' * (5 - len(str(test_stat_obj.total_tested))))
        output += test_stat_obj.test_name
        return output