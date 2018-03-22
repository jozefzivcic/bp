from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart


class FilteredItemDto:
    def __init__(self, ds_info: DataSourceInfo, p_value: float, condition_fulfilled: bool):
        if ds_info.tests_in_chart != TestsInChart.PAIR_OF_TESTS:
            raise ValueError('Wrong type of DataSourceInfo.tests_in_chart. Expected PAIR_OF_TESTS, got: {}'
                             .format(ds_info.tests_in_chart))
        if p_value < 0.0 or p_value > 1.0:
            raise ValueError('p-value must be in interval [0.0-1.0]. But {} was given'.format(p_value))
        self.ds_info = ds_info
        self.p_value = p_value
        self.condition_fulfilled = condition_fulfilled

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(self, other.__class__):
            return False
        diff = abs(self.p_value - other.p_value)
        threshold = 1E-6
        return self.ds_info == other.ds_info and diff < threshold and \
               self.condition_fulfilled == other.condition_fulfilled
