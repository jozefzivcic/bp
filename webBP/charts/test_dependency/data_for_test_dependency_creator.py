from charts.test_dependency_dto import TestDependencyDto
from p_value_processing.p_values_accumulator import PValuesAccumulator


class DataForTestDependencyCreator:
    def __init__(self, test_dependency_dto: TestDependencyDto=None, acc: PValuesAccumulator=None, directory: str=None,
                 file_id: int=None):
        self.test_dependency_dto = test_dependency_dto
        self.acc = acc
        self.directory = directory
        self.file_id = file_id
