from unittest import TestCase

from charts.ecdf.ecdf_extractor import EcdfExtractor
from charts.ecdf_dto import EcdfDto
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14, TestsIdData


class TestEcdfExtractor(TestCase):
    def setUp(self):
        self.ecdf_extractor = EcdfExtractor()
        self.ecdf_dto = EcdfDto(0.5, 'title', 'x_label', 'y_label', 'empirical_label', 'theoretical_label')
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        self.acc = PValuesAccumulator()
        self.acc.add(TestsIdData.test1_id, dto_13)
        self.acc.add(TestsIdData.test2_id, dto_14)

    def test_get_data_from_accumulator_results_file_type(self):
        self.ecdf_dto.sequence = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        ret = self.ecdf_extractor.get_data_from_accumulator(self.acc, self.ecdf_dto)

        self.assertEqual(self.ecdf_dto.alpha, ret.alpha)
        self.assertEqual(self.ecdf_dto.title, ret.title)
        self.assertEqual(self.ecdf_dto.x_label, ret.x_label)
        self.assertEqual(self.ecdf_dto.y_label, ret.y_label)
        self.assertEqual(self.ecdf_dto.empirical_label, ret.empirical_label)
        self.assertEqual(self.ecdf_dto.theoretical_label, ret.theoretical_label)
        self.assertEqual(dict_for_test_13['results'], ret.p_values)

    def test_get_data_from_accumulator_data_file_type(self):
        self.ecdf_dto.sequence = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        ret = self.ecdf_extractor.get_data_from_accumulator(self.acc, self.ecdf_dto)

        self.assertEqual(self.ecdf_dto.alpha, ret.alpha)
        self.assertEqual(self.ecdf_dto.title, ret.title)
        self.assertEqual(self.ecdf_dto.x_label, ret.x_label)
        self.assertEqual(self.ecdf_dto.y_label, ret.y_label)
        self.assertEqual(self.ecdf_dto.empirical_label, ret.empirical_label)
        self.assertEqual(self.ecdf_dto.theoretical_label, ret.theoretical_label)
        self.assertEqual(dict_for_test_14['data2'], ret.p_values)

    def test_get_data_from_accumulator_wrong_file_type(self):
        self.ecdf_dto.sequence = PValueSequence(TestsIdData.test2_id, 3)
        with self.assertRaises(ValueError) as ex:
            self.ecdf_extractor.get_data_from_accumulator(self.acc, self.ecdf_dto)
        self.assertEqual('Unsupported file type 3', str(ex.exception))
