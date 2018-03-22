from unittest import TestCase

from copy import deepcopy

from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart
from p_value_processing.data_from_filter_pairs import DataFromFilterPairs
from p_value_processing.filtered_item_dto import FilteredItemDto
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import TestsIdData


class TestDataFromFilterPairs(TestCase):
    def setUp(self):
        self.data_from_fp = DataFromFilterPairs()
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        self.item_dto1 = FilteredItemDto(ds_info, 0.456, True)

        seq1 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 1)
        seq2 = PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        self.item_dto2 = FilteredItemDto(ds_info, 0.654, True)

        seq1 = PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS)
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        self.item_dto3 = FilteredItemDto(ds_info, 0.753, False)

    def test_add_kept(self):
        self.data_from_fp.add_kept(self.item_dto1)
        ret = self.data_from_fp.get_kept()
        self.assertEqual([deepcopy(self.item_dto1)], ret)
        self.assertFalse(self.data_from_fp.get_deleted())

        self.data_from_fp.add_kept(self.item_dto2)
        ret = self.data_from_fp.get_kept()
        self.assertEqual([deepcopy(self.item_dto1), deepcopy(self.item_dto2)], ret)
        self.assertFalse(self.data_from_fp.get_deleted())

    def test_add_deleted(self):
        self.data_from_fp.add_deleted(self.item_dto1)
        ret = self.data_from_fp.get_deleted()
        self.assertEqual([deepcopy(self.item_dto1)], ret)
        self.assertFalse(self.data_from_fp.get_kept())

        self.data_from_fp.add_deleted(self.item_dto2)
        ret = self.data_from_fp.get_deleted()
        self.assertEqual([deepcopy(self.item_dto1), deepcopy(self.item_dto2)], ret)
        self.assertFalse(self.data_from_fp.get_kept())

    def test_add_kept_and_deleted(self):
        self.data_from_fp.add_kept(self.item_dto1)
        self.data_from_fp.add_deleted(self.item_dto2)

        ret = self.data_from_fp.get_kept()
        self.assertEqual([deepcopy(self.item_dto1)], ret)

        ret = self.data_from_fp.get_deleted()
        self.assertEqual([deepcopy(self.item_dto2)], ret)

    def test_are_not_equal(self):
        self.data_from_fp.add_kept(self.item_dto1)

        another_data = DataFromFilterPairs()
        self.assertNotEqual(self.data_from_fp, another_data)
        self.assertTrue(self.data_from_fp != another_data)

        another_data.add_deleted(deepcopy(self.item_dto2))
        self.assertNotEqual(self.data_from_fp, another_data)
        self.assertTrue(self.data_from_fp != another_data)

        another_data.add_kept(deepcopy(self.item_dto1))
        self.assertNotEqual(self.data_from_fp, another_data)
        self.assertTrue(self.data_from_fp != another_data)

    def test_are_equal(self):
        another_data = DataFromFilterPairs()
        self.assertEqual(self.data_from_fp, another_data)
        self.assertTrue(self.data_from_fp == another_data)

        self.data_from_fp.add_kept(self.item_dto1)
        another_data.add_kept(deepcopy(self.item_dto1))
        self.assertEqual(self.data_from_fp, another_data)
        self.assertTrue(self.data_from_fp == another_data)

        self.data_from_fp.add_kept(self.item_dto2)
        another_data.add_kept(deepcopy(self.item_dto2))
        self.assertEqual(self.data_from_fp, another_data)
        self.assertTrue(self.data_from_fp == another_data)

        self.data_from_fp.add_deleted(self.item_dto3)
        another_data.add_deleted(deepcopy(self.item_dto3))
        self.assertEqual(self.data_from_fp, another_data)
        self.assertTrue(self.data_from_fp == another_data)
