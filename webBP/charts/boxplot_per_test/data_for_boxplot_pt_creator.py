from charts.boxplot_pt_dto import BoxplotPTDto
from p_value_processing.p_values_accumulator import PValuesAccumulator


class DataForBoxplotPTCreator:
    def __init__(self, dto: BoxplotPTDto, acc: PValuesAccumulator, directory: str, file_id: int):
        self.dto = dto
        self.acc = acc
        self.directory = directory
        self.file_id = file_id
