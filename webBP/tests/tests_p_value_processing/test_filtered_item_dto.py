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
            FilteredItemDto(ds_info, True)
        self.assertEqual('Wrong type of DataSourceInfo.tests_in_chart. Expected PAIR_OF_TESTS, got: '
                         'TestsInChart.SINGLE_TEST', str(ex.exception))

    def test_are_not_eq_different_ds_info(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto1 = FilteredItemDto(ds_info, False)

        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(457, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto2 = FilteredItemDto(ds_info, False)
        self.assertNotEqual(dto1, dto2)
        self.assertTrue(dto1 != dto2)

    def test_are_not_eq_different_condition(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto1 = FilteredItemDto(ds_info, True)

        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto2 = FilteredItemDto(ds_info, False)
        self.assertNotEqual(dto1, dto2)
        self.assertTrue(dto1 != dto2)

    def test_are_equal(self):
        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto1 = FilteredItemDto(ds_info, False)

        seq1 = PValueSequence(1, PValuesFileType.RESULTS)
        seq2 = PValueSequence(456, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        dto2 = FilteredItemDto(ds_info, False)
        self.assertEqual(dto1, dto2)

        self.assertFalse(dto1 != dto2)