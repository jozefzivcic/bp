from unittest import TestCase

from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto


class TestPValuesAccumulator(TestCase):
    def setUp(self):
        self.dto1 = PValuesDto({'results': [0.0, 0.1, 0.2]})
        self.dto2 = PValuesDto({'results': [0.3, 0.4, 0.5, 0.6], 'data1': [0.3, 0.5], 'data2': [0.4, 0.6]})
        self.test1_id = 789
        self.test2_id = 1234
        self.accumulator = PValuesAccumulator()

    def test_add_one_dto(self):
        self.accumulator.add(self.test1_id, self.dto1)
        ret = self.accumulator.get_dto_for_test(self.test1_id)
        self.assertEqual(self.dto1, ret)

    def test_add_two_dtos(self):
        self.accumulator.add(self.test1_id, self.dto1)
        self.accumulator.add(self.test2_id, self.dto2)

        ret = self.accumulator.get_dto_for_test(self.test1_id)
        self.assertEqual(self.dto1, ret)

        ret = self.accumulator.get_dto_for_test(self.test2_id)
        self.assertEqual(self.dto2, ret)

    def test_add_with_same_test_id(self):
        self.accumulator.add(self.test1_id, self.dto1)
        with self.assertRaises(ValueError) as context:
            self.accumulator.add(self.test1_id, self.dto1)
            self.assertTrue(str(self.test1_id) in str(context.exception))

    def test_get_with_non_existing_test_id(self):
        self.accumulator.add(self.test1_id, self.dto1)
        with self.assertRaises(ValueError) as context:
            self.accumulator.get_dto_for_test(self.test2_id)
            self.assertTrue(str(self.test2_id) in str(context.exception))