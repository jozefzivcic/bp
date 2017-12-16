from unittest import TestCase

from p_value_processing.processing_dto import ProcessingDto


class TestProcessingDto(TestCase):
    def setUp(self):
        self.arr = [(1, 'one'), (2, 'two'), (3, 'three')]
        self.dto = ProcessingDto()

    def test_add_and_iterate(self):
        for first, second in self.arr:
            self.dto.add(first, second)
        ret = []

        for first, second in self.dto:
            ret.append((first, second))

        self.assertEqual(self.arr, ret)
