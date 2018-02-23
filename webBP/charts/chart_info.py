from charts.chart_type import ChartType
from charts.data_source_info import DataSourceInfo


class ChartInfo:
    def __init__(self, ds_info: DataSourceInfo=None, path: str=None, chart_type: ChartType=None, file_id: int=None):
        self.ds_info = ds_info
        self.path_to_chart = path
        self.chart_type = chart_type
        self.file_id = file_id

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.ds_info == other.ds_info and self.path_to_chart == other.path_to_chart and \
               self.chart_type == other.chart_type and self.file_id == other.file_id
