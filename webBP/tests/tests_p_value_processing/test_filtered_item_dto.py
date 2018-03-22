from unittest import TestCase

from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart
from p_value_processing.filtered_item_dto import FilteredItemDto
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType


class TestFilteredItemDto(TestCase):
    def test_wrong_ds_info(self):
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, PValueSequence(1, PValuesFileType.RESULTS))
        with self.assertRaises(ValueError) as ex:
            FilteredItemDto(ds_info, 0.456, True)
        self.assertEqual('Wrong type of DataSourceInfo.tests_in_chart. Expected PAIR_OF_TESTS, got: '
                         'TestsInChart.SINGLE_TEST', str(ex.exception))

    def test_negative_p_value(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        with self.assertRaises(ValueError) as ex:
            FilteredItemDto(ds_info, -0.000001, True)
        self.assertEqual('p-value must be in interval [0.0-1.0]. But -1e-06 was given', str(ex.exception))

    def test_p_value_too_big(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        with self.assertRaises(ValueError) as ex:
            FilteredItemDto(ds_info, 1.000001, True)
        self.assertEqual('p-value must be in interval [0.0-1.0]. But 1.000001 was given', str(ex.exception))

    def test_p_value_ok(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        FilteredItemDto(ds_info, 0.0, True)
        FilteredItemDto(ds_info, 0.5, True)
        FilteredItemDto(ds_info, 1.0, True)

    def test_are_not_eq_different_ds_info(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto1 = FilteredItemDto(ds_info, 0.5, False)

        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(457, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto2 = FilteredItemDto(ds_info, 0.5, False)
        self.assertNotEqual(dto1, dto2)
        self.assertTrue(dto1 != dto2)

    def test_are_not_eq_different_p_value(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto1 = FilteredItemDto(ds_info, 0.5678, True)

        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto2 = FilteredItemDto(ds_info, 0.5679, False)
        self.assertNotEqual(dto1, dto2)
        self.assertTrue(dto1 != dto2)

    def test_are_not_eq_different_condition(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto1 = FilteredItemDto(ds_info, 0.5, True)

        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto2 = FilteredItemDto(ds_info, 0.5, False)
        self.assertNotEqual(dto1, dto2)
        self.assertTrue(dto1 != dto2)

    def test_are_equal(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto1 = FilteredItemDto(ds_info, 0.5, False)

        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto2 = FilteredItemDto(ds_info, 0.5, False)
        self.assertEqual(dto1, dto2)

        self.assertFalse(dto1 != dto2)
