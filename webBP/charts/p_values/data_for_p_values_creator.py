from charts.chart_options import ChartOptions
from p_value_processing.p_values_accumulator import PValuesAccumulator


class DataForPValuesCreator:
    def __init__(self, chart_options: ChartOptions, acc: PValuesAccumulator, directory: str, file_id: int):
        self.chart_options = chart_options
        self.acc = acc
        self.directory = directory
        self.file_id = file_id
