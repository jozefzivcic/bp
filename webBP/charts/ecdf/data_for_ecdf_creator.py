from charts.dto.ecdf_dto import EcdfDto
from p_value_processing.p_values_accumulator import PValuesAccumulator


class DataForEcdfCreator:
    def __init__(self, ecdf_dto: EcdfDto=None, acc: PValuesAccumulator=None, directory: str=None,
                 file_id: int=None):
        self.ecdf_dto = ecdf_dto
        self.acc = acc
        self.directory = directory
        self.file_id = file_id
