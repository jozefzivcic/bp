from charts.p_values_chart_dto import PValuesChartDto
from p_value_processing.p_values_accumulator import PValuesAccumulator


class DataForPValuesCreator:
    def __init__(self, dto: PValuesChartDto, acc: PValuesAccumulator, directory: str, file_id: int):
        self.chart_options = dto
        self.acc = acc
        self.directory = directory
        self.file_id = file_id
