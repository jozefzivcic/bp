from nist_statistics.helpers import get_proportion_threshold_min, get_proportion_threshold_max
from nist_statistics.test_statistics_dto import TestStatisticsDTO


class LineGenerator:
    def generate_line_from_test_statistics(self, test_stat_obj: TestStatisticsDTO) -> str:
        output = ''
        for num in test_stat_obj.p_value_array:
            output += '%3d ' % num

        if test_stat_obj.exp_count == 0:
            output += '    ----    '
        elif test_stat_obj.uniformity_p_value < 0.0001:
            output += ' %8.6f * ' % test_stat_obj.uniformity_p_value
        else:
            output += ' %8.6f   ' % test_stat_obj.uniformity_p_value

        if test_stat_obj.exp_count == 0:
            output += '    ----    '
        elif test_stat_obj.KS_p_value < 0.0001:
            output += ' %8.6f * ' % test_stat_obj.KS_p_value
        else:
            output += ' %8.6f   ' % test_stat_obj.KS_p_value

        if test_stat_obj.sample_size == 0:
            output += ' ----     ' + test_stat_obj.test_name
        elif (test_stat_obj.proportion < get_proportion_threshold_min(test_stat_obj)) or \
                (test_stat_obj.proportion > get_proportion_threshold_max(test_stat_obj)):
            output += '%6.4f *  ' % test_stat_obj.proportion
            output += test_stat_obj.test_name
        else:
            output += '%6.4f    ' % test_stat_obj.proportion
            output += test_stat_obj.test_name

        return output
