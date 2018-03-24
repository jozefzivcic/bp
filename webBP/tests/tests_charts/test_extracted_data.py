from unittest import TestCase
from unittest.mock import MagicMock

from copy import deepcopy

from charts.data_source_info import DataSourceInfo
from charts.extracted_data import ExtractedData
from charts.tests_in_chart import TestsInChart
from common.error.test_dep_seq_len_err import TestDepSeqLenErr
from common.info.test_dep_filtered_info import TestDepFilteredInfo
from common.info.test_dep_unif_info import TestDepUnifInfo
from enums.filter_uniformity import FilterUniformity
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import TestsIdData


class TestExtractedData(TestCase):
    def test_add_data(self):
        ex_data = ExtractedData()
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        ds_info1 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq1)
        data_for_drawer1 = MagicMock(key1='value1', key2='value2')
        info1 = TestDepUnifInfo(0.5, False)

        ex_data.add_data(ds_info1, data_for_drawer1, info1)

        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        ds_info2 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq2)
        data_for_drawer2 = MagicMock(key3='value3', key4='value4')
        err2 = TestDepSeqLenErr(None, 4, None, 5)

        ex_data.add_data(ds_info2, data_for_drawer2, None, err2)

        ret = ex_data.get_all_data()

        quadruple = ret[0]
        self.assertEqual(deepcopy(ds_info1), quadruple[0])
        self.assertEqual(deepcopy(data_for_drawer1), quadruple[1])
        self.assertEqual(deepcopy(info1), quadruple[2])
        self.assertIsNone(quadruple[3])

        quadruple = ret[1]
        self.assertEqual(deepcopy(ds_info2), quadruple[0])
        self.assertEqual(deepcopy(data_for_drawer2), quadruple[1])
        self.assertIsNone(quadruple[2])
        self.assertEqual(deepcopy(err2), quadruple[3])

    def test_add_info(self):
        info1 = TestDepFilteredInfo(4, 5, FilterUniformity.REMOVE_NON_UNIFORM)
        ex_data = ExtractedData()
        ex_data.add_info(info1)

        ret = ex_data.get_all_infos()
        self.assertEqual(1, len(ret))
        self.assertEqual(deepcopy(info1), ret[0])

        info2 = TestDepFilteredInfo(5, 10, FilterUniformity.REMOVE_UNIFORM)
        ex_data.add_info(info2)

        ret = ex_data.get_all_infos()
        self.assertEqual(2, len(ret))
        self.assertEqual(deepcopy(info1), ret[0])
        self.assertEqual(deepcopy(info2), ret[1])

    def test_add_err(self):
        err1 = TestDepSeqLenErr(None, 4, None, 5)
        ex_data = ExtractedData()
        ex_data.add_err(err1)

        ret = ex_data.get_all_errs()
        self.assertEqual(1, len(ret))
        self.assertEqual(deepcopy(err1), ret[0])

        err2 = TestDepSeqLenErr(None, 2, None, 10)
        ex_data.add_err(err2)

        ret = ex_data.get_all_errs()
        self.assertEqual(2, len(ret))
        self.assertEqual(deepcopy(err1), ret[0])
        self.assertEqual(deepcopy(err2), ret[1])

    def test_add_all_types(self):
        ex_data = ExtractedData()
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        ds_info1 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq1)
        data_for_drawer1 = MagicMock(key1='value1', key2='value2')
        info1 = TestDepUnifInfo(0.5, False)
        err1 = TestDepSeqLenErr(None, 4, None, 5)

        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        ds_info2 = DataSourceInfo(TestsInChart.SINGLE_TEST, seq2)
        data_for_drawer2 = MagicMock(key3='value3', key4='value4')

        ex_data.add_data(ds_info1, data_for_drawer1, info1, err1)
        ex_data.add_data(ds_info2, data_for_drawer2)

        separate_info = TestDepUnifInfo(0.456, True)
        separate_err = TestDepSeqLenErr(None, 456, None, 4567)

        ex_data.add_info(separate_info)
        ex_data.add_err(separate_err)

        ret = ex_data.get_all_data()
        self.assertEqual(2, len(ret))
        quadruple = ret[0]
        self.assertEqual(deepcopy(ds_info1), quadruple[0])
        self.assertEqual(deepcopy(data_for_drawer1), quadruple[1])
        self.assertEqual(deepcopy(info1), quadruple[2])
        self.assertEqual(deepcopy(err1), quadruple[3])

        quadruple = ret[1]
        self.assertEqual(deepcopy(ds_info2), quadruple[0])
        self.assertEqual(deepcopy(data_for_drawer2), quadruple[1])
        self.assertIsNone(quadruple[2])
        self.assertIsNone(quadruple[3])

        ret = ex_data.get_all_infos()
        self.assertEqual(1, len(ret))
        self.assertEqual(deepcopy(separate_info), ret[0])

        ret = ex_data.get_all_errs()
        self.assertEqual(1, len(ret))
        self.assertEqual(deepcopy(separate_err), ret[0])
