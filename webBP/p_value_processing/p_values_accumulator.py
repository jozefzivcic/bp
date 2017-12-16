from p_value_processing.p_values_dto import PValuesDto


class PValuesAccumulator:
    def __init__(self):
        self.objects = {}

    def add(self, test_id: int, dto: PValuesDto):
        if test_id in self.objects:
            raise ValueError('test_id: ' + str(test_id) + ' already used')
        self.objects[test_id] = dto

    def get_dto_for_test(self, test_id: int) -> PValuesDto:
        if not test_id in self.objects:
            raise ValueError('No DTO for test with id: ' + str(test_id))
        return self.objects[test_id]