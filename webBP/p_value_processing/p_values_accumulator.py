from p_value_processing.p_values_dto import PValuesDto


class PValuesAccumulator:
    def __init__(self):
        self._objects = {}

    def add(self, test_id: int, dto: PValuesDto):
        if test_id in self._objects:
            raise ValueError('test_id: ' + str(test_id) + ' already used')
        self._objects[test_id] = dto

    def get_dto_for_test(self, test_id: int) -> PValuesDto:
        if not test_id in self._objects:
            raise ValueError('No DTO for test with id: ' + str(test_id))
        return self._objects[test_id]

    def get_all_test_ids(self) -> list:
        return sorted(self._objects.keys())
