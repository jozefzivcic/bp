from charts.dto.proportions_dto import ProportionsDto
from p_value_processing.p_values_accumulator import PValuesAccumulator


class DatForProportionsCreator(object):
    def __init__(self, prop_dto: ProportionsDto=None, acc: PValuesAccumulator=None, directory: str=None,
                 file_id: int=None):
        self.prop_dto = prop_dto
        self.acc = acc
        self.directory = directory
        self.file_id = file_id
