from charts.histogram_dto import HistogramDto
from p_value_processing.p_values_accumulator import PValuesAccumulator


class DataForHistogramCreator:
    def __init__(self, histogram_dto: HistogramDto, acc: PValuesAccumulator, directory: str, file_id: int):
        self.histogram_dto = histogram_dto
        self.acc = acc
        self.directory = directory
        self.file_id = file_id
