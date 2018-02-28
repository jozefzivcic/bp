from p_value_processing.p_values_dto import PValuesDto


class PValuesAccumulator:
    def __init__(self):
        self._objects = {}

    def add(self, test_id: int, dto: PValuesDto):
        if test_id in self._objects:
            raise ValueError('test_id: ' + str(test_id) + ' already used')
        self._objects[test_id] = dto

    def get_dto_for_test(self, test_id: int) -> PValuesDto:
        ret = self.get_dto_for_test_safe(test_id)
        if ret is None:
            raise ValueError('No DTO for test with id: ' + str(test_id))
        return ret

    def get_dto_for_test_safe(self, test_id: int) -> PValuesDto:
        return self._objects.get(test_id, None)

    def get_all_test_ids(self) -> list:
        return sorted(self._objects.keys())
