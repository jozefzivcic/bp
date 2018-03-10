from charts.data_source_info import DataSourceInfo


class FilteredItemDto:
    def __init__(self, ds_info: DataSourceInfo, condition_fulfilled: bool):
        self.ds_info = ds_info
        self.condition_fulfilled = condition_fulfilled
