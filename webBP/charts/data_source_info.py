from charts.tests_in_chart import TestsInChart
from p_value_processing.p_value_sequence import PValueSequence


class DataSourceInfo:
    def __init__(self, tests_in_chart: TestsInChart=None, p_value_sequence=None):
        self.tests_in_chart = tests_in_chart
        if tests_in_chart == TestsInChart.SINGLE_TEST and type(p_value_sequence) != PValueSequence:
            raise ValueError(self.get_error_message(tests_in_chart, p_value_sequence))
        if tests_in_chart == TestsInChart.PAIR_OF_TESTS and type(p_value_sequence) != tuple:
            raise ValueError(self.get_error_message(tests_in_chart, p_value_sequence))
        if tests_in_chart == TestsInChart.PAIR_OF_TESTS and len(p_value_sequence) != 2:
            raise ValueError('Tuple should contain exactly two PValueSequence objects for TestsInChart.PAIR_OF_TESTS')
        if tests_in_chart == TestsInChart.MULTIPLE_TESTS and type(p_value_sequence) != list:
            raise ValueError(self.get_error_message(tests_in_chart, p_value_sequence))
        if tests_in_chart == TestsInChart.MULTIPLE_TESTS and len(p_value_sequence) == 0:
            raise ValueError('Multiple tests cannot have empty list')
        self.p_value_sequence = p_value_sequence

    def get_error_message(self, tests_in_chart, p_value_sequence):
        return 'Arguments tests_in_chart: {} and p_value_sequence {} are not alowed' \
            .format(tests_in_chart, str(type(p_value_sequence)))

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.tests_in_chart == other.tests_in_chart and self.p_value_sequence == other.p_value_sequence
