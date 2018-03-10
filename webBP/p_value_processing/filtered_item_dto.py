from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart


class FilteredItemDto:
    def __init__(self, ds_info: DataSourceInfo, condition_fulfilled: bool):
        if ds_info.tests_in_chart != TestsInChart.PAIR_OF_TESTS:
            raise ValueError('Wrong type of DataSourceInfo.tests_in_chart. Expected PAIR_OF_TESTS, got: {}'
                             .format(ds_info.tests_in_chart))
        self.ds_info = ds_info
        self.condition_fulfilled = condition_fulfilled

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(self, other.__class__):
            return False
        return self.ds_info == other.ds_info and self.condition_fulfilled == other.condition_fulfilled
