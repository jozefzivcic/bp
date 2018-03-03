from unittest import TestCase

from copy import deepcopy

from charts.data_source_info import DataSourceInfo
from charts.ecdf.ecdf_extractor import EcdfExtractor
from charts.dto.ecdf_dto import EcdfDto
from charts.tests_in_chart import TestsInChart
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
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq_copy = deepcopy(seq)
        self.ecdf_dto.sequences = [seq]
        extracted_data = self.ecdf_extractor.get_data_from_accumulator(self.acc, self.ecdf_dto)

        self.assertEqual(1, len(extracted_data))
        ret = extracted_data[0].ds_info
        expected = DataSourceInfo(TestsInChart.SINGLE_TEST, seq_copy)
        self.assertEqual(expected, ret)

        ret = extracted_data[0].data_for_drawer
        self.assertEqual(self.ecdf_dto.alpha, ret.alpha)
        self.assertEqual(self.ecdf_dto.title, ret.title)
        self.assertEqual(self.ecdf_dto.x_label, ret.x_label)
        self.assertEqual(self.ecdf_dto.y_label, ret.y_label)
        self.assertEqual(self.ecdf_dto.empirical_label, ret.empirical_label)
        self.assertEqual(self.ecdf_dto.theoretical_label, ret.theoretical_label)
        self.assertEqual(dict_for_test_13['results'], ret.p_values)

    def test_get_data_from_accumulator_data_file_type(self):
        seq = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        seq_copy = deepcopy(seq)
        self.ecdf_dto.sequences = [seq]
        extracted_data = self.ecdf_extractor.get_data_from_accumulator(self.acc, self.ecdf_dto)

        self.assertEqual(1, len(extracted_data))

        ret = extracted_data[0].ds_info
        expected = DataSourceInfo(TestsInChart.SINGLE_TEST, seq_copy)
        self.assertEqual(expected, ret)

        ret = extracted_data[0].data_for_drawer
        self.assertEqual(self.ecdf_dto.alpha, ret.alpha)
        self.assertEqual(self.ecdf_dto.title, ret.title)
        self.assertEqual(self.ecdf_dto.x_label, ret.x_label)
        self.assertEqual(self.ecdf_dto.y_label, ret.y_label)
        self.assertEqual(self.ecdf_dto.empirical_label, ret.empirical_label)
        self.assertEqual(self.ecdf_dto.theoretical_label, ret.theoretical_label)
        self.assertEqual(dict_for_test_14['data2'], ret.p_values)

    def test_get_data_from_accumulator_two_sequences(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        seq1_copy = deepcopy(seq1)
        seq2_copy = deepcopy(seq2)

        self.ecdf_dto.sequences = [seq1, seq2]
        extracted_data = self.ecdf_extractor.get_data_from_accumulator(self.acc, self.ecdf_dto)

        self.assertEqual(2, len(extracted_data))

        ret = extracted_data[0].ds_info
        expected = DataSourceInfo(TestsInChart.SINGLE_TEST, seq1_copy)
        self.assertEqual(expected, ret)

        ret = extracted_data[1].ds_info
        expected = DataSourceInfo(TestsInChart.SINGLE_TEST, seq2_copy)
        self.assertEqual(expected, ret)

        ret = extracted_data[0].data_for_drawer

        self.assertEqual(self.ecdf_dto.alpha, ret.alpha)
        self.assertEqual(self.ecdf_dto.title, ret.title)
        self.assertEqual(self.ecdf_dto.x_label, ret.x_label)
        self.assertEqual(self.ecdf_dto.y_label, ret.y_label)
        self.assertEqual(self.ecdf_dto.empirical_label, ret.empirical_label)
        self.assertEqual(self.ecdf_dto.theoretical_label, ret.theoretical_label)
        self.assertEqual(dict_for_test_13['results'], ret.p_values)

        ret = extracted_data[1].data_for_drawer

        self.assertEqual(self.ecdf_dto.alpha, ret.alpha)
        self.assertEqual(self.ecdf_dto.title, ret.title)
        self.assertEqual(self.ecdf_dto.x_label, ret.x_label)
        self.assertEqual(self.ecdf_dto.y_label, ret.y_label)
        self.assertEqual(self.ecdf_dto.empirical_label, ret.empirical_label)
        self.assertEqual(self.ecdf_dto.theoretical_label, ret.theoretical_label)
        self.assertEqual(dict_for_test_14['data2'], ret.p_values)

    def test_get_data_accumulator_contains_only_two_sequences(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        seq3 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 1)
        seq1_copy = deepcopy(seq1)
        seq2_copy = deepcopy(seq2)

        self.ecdf_dto.sequences = [seq1, seq2, seq3]
        extracted_data = self.ecdf_extractor.get_data_from_accumulator(self.acc, self.ecdf_dto)

        self.assertEqual(2, len(extracted_data))

        ret = extracted_data[0].ds_info
        expected = DataSourceInfo(TestsInChart.SINGLE_TEST, seq1_copy)
        self.assertEqual(expected, ret)

        ret = extracted_data[1].ds_info
        expected = DataSourceInfo(TestsInChart.SINGLE_TEST, seq2_copy)
        self.assertEqual(expected, ret)

        ret = extracted_data[0].data_for_drawer

        self.assertEqual(self.ecdf_dto.alpha, ret.alpha)
        self.assertEqual(self.ecdf_dto.title, ret.title)
        self.assertEqual(self.ecdf_dto.x_label, ret.x_label)
        self.assertEqual(self.ecdf_dto.y_label, ret.y_label)
        self.assertEqual(self.ecdf_dto.empirical_label, ret.empirical_label)
        self.assertEqual(self.ecdf_dto.theoretical_label, ret.theoretical_label)
        self.assertEqual(dict_for_test_13['results'], ret.p_values)

        ret = extracted_data[1].data_for_drawer

        self.assertEqual(self.ecdf_dto.alpha, ret.alpha)
        self.assertEqual(self.ecdf_dto.title, ret.title)
        self.assertEqual(self.ecdf_dto.x_label, ret.x_label)
        self.assertEqual(self.ecdf_dto.y_label, ret.y_label)
        self.assertEqual(self.ecdf_dto.empirical_label, ret.empirical_label)
        self.assertEqual(self.ecdf_dto.theoretical_label, ret.theoretical_label)
        self.assertEqual(dict_for_test_14['data2'], ret.p_values)

    def test_get_data_accumulator_contains_none_of_sequences(self):
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        seq3 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 1)
        self.ecdf_dto.sequences = [seq1, seq2, seq3]

        acc = PValuesAccumulator()
        ret = self.ecdf_extractor.get_data_from_accumulator(acc, self.ecdf_dto)
        self.assertEqual(0, len(ret))

    def test_get_data_from_accumulator_wrong_file_type(self):
        self.ecdf_dto.sequences = [PValueSequence(TestsIdData.test2_id, 3)]
        with self.assertRaises(ValueError) as ex:
            self.ecdf_extractor.get_data_from_accumulator(self.acc, self.ecdf_dto)
        self.assertEqual('Unsupported file type 3', str(ex.exception))
