import json
from collections import OrderedDict
from copy import deepcopy
from unittest import TestCase
from unittest.mock import MagicMock, patch

from charts.boxplot_per_test.boxplot_pt_extractor import BoxplotPTExtractor
from charts.data_source_info import DataSourceInfo
from charts.different_num_of_pvals_error import DifferentNumOfPValsError
from charts.dto.boxplot_pt_dto import BoxplotPTDto
from charts.tests_in_chart import TestsInChart
from common.error.diff_pvalues_len_err import DiffPValuesLenErr
from models.nistparam import NistParam
from models.test import Test
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import TestsIdData, dict_for_test_13, dict_for_test_41, dict_for_test_14, \
    dict_for_test_42, dict_for_test_43, short_names_dict
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test, \
    func_prepare_acc


def get_name_from_seq(seq: PValueSequence, test_names) -> str:
    name = '({})'.format(seq.test_id)
    if seq.p_values_file == PValuesFileType.DATA:
        name += ' data {}'.format(seq.data_num)
    return name


class TestBoxplotPTExtractor(TestCase):
    def mock_func(self, func_name, side_effect):
        patcher = patch(func_name, side_effect=side_effect)
        self.addCleanup(patcher.stop)
        patcher.start()

    def mock(self):
        self.mock_func('managers.dbtestmanager.DBTestManager.get_test_by_id', db_test_dao_get_test_by_id)
        self.mock_func('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                       nist_dao_get_nist_param_for_test)

    def setUp(self):
        self.mock()
        storage = MagicMock(nist='nist')
        self.extractor = BoxplotPTExtractor(None, storage)

    @patch('charts.boxplot_per_test.boxplot_pt_extractor.BoxplotPTExtractor.get_name_from_seq',
           side_effect=get_name_from_seq)
    def test_get_data_from_accumulator(self, f_get_name):
        acc = func_prepare_acc()
        seqcs = [[PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS),
                  PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1),
                  PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)],
                 [PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS),
                  PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS)]]
        dto = BoxplotPTDto('Boxplot(s) for tests', seqcs, short_names_dict)
        ex_data = self.extractor.get_data_from_accumulator(acc, dto)
        ex_data_list = ex_data.get_all_data()
        self.assertEqual(2, len(ex_data_list))

        expected_dict = OrderedDict([('({})'.format(TestsIdData.test1_id), dict_for_test_13['results']),
                                     ('({}) data 1'.format(TestsIdData.test2_id), dict_for_test_14['data1']),
                                     ('({}) data 2'.format(TestsIdData.test3_id), dict_for_test_41['data2'])])
        expected_str = json.dumps(expected_dict)
        quadruple = ex_data_list[0]
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, deepcopy(seqcs[0]))
        self.assertEqual(ds_info, quadruple[0])
        drawer_data = quadruple[1]
        self.assertEqual(dto.title, drawer_data.title)
        self.assertEqual(expected_str, drawer_data.json_data_str)

        expected_dict = OrderedDict([('({})'.format(TestsIdData.test4_id), dict_for_test_42['results']),
                                     ('({})'.format(TestsIdData.test5_id), dict_for_test_43['results'])])
        expected_str = json.dumps(expected_dict)
        quadruple = ex_data_list[1]
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, deepcopy(seqcs[1]))
        self.assertEqual(ds_info, quadruple[0])
        drawer_data = quadruple[1]
        self.assertEqual(dto.title, drawer_data.title)
        self.assertEqual(expected_str, drawer_data.json_data_str)

    @patch('charts.boxplot_per_test.boxplot_pt_extractor.BoxplotPTExtractor.get_name_from_seq',
           side_effect=get_name_from_seq)
    def test_get_data_from_accumulator_skip_seq(self, f_get_name):
        acc = func_prepare_acc()
        seqcs = [[PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS),
                  PValueSequence(TestsIdData.non_existing_test_id, PValuesFileType.DATA, 1)]]
        dto = BoxplotPTDto('Boxplot(s) for tests', seqcs, short_names_dict)
        ex_data = self.extractor.get_data_from_accumulator(acc, dto)
        ex_data_list = ex_data.get_all_data()
        self.assertEqual(1, len(ex_data_list))

        expected_dict = {'({})'.format(TestsIdData.test1_id): dict_for_test_13['results']}
        expected_str = json.dumps(expected_dict)
        quadruple = ex_data_list[0]
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, [PValueSequence(TestsIdData.test1_id,
                                                                              PValuesFileType.RESULTS)])
        self.assertEqual(ds_info, quadruple[0])
        drawer_data = quadruple[1]
        self.assertEqual(dto.title, drawer_data.title)
        self.assertEqual(expected_str, drawer_data.json_data_str)
        f_get_name.assert_called_once_with(PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS),
                                           short_names_dict)

    @patch('charts.boxplot_per_test.boxplot_pt_extractor.BoxplotPTExtractor.create_extracted_data',
           side_effect=DifferentNumOfPValsError('message', 15, 4))
    def test_get_data_from_accumulator_create_raises(self, f_create):
        mock = MagicMock(name='PValuesAccumulator')
        dto = BoxplotPTDto('title', ['seq1', 'seq2'])
        ret = self.extractor.get_data_from_accumulator(mock, dto)
        self.assertEqual([], ret.get_all_data())
        self.assertEqual([], ret.get_all_infos())
        err = DiffPValuesLenErr(15, 4)
        self.assertEqual([err], ret.get_all_errs())
        f_create.assert_called_once_with(mock, 'seq1', dto)

    @patch('charts.boxplot_per_test.boxplot_pt_extractor.BoxplotPTExtractor.get_p_values', return_value=[1, 2, 3])
    def test_create_extracted_data_raises(self, f_get_p_values):
        mock = MagicMock(some_id='some id')
        seqcs = [PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS),
                 PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)]
        with self.assertRaises(DifferentNumOfPValsError) as ex:
            self.extractor.create_extracted_data(mock, seqcs, None)
        self.assertEqual('Expected 10 p-values, found only 3.', str(ex.exception))
        self.assertEqual(10, ex.exception.expected_len)
        self.assertEqual(3, ex.exception.actual_len)
        f_get_p_values.assert_called_once_with(mock, seqcs[0])

    @patch('charts.boxplot_per_test.boxplot_pt_extractor.BoxplotPTExtractor.get_name_from_seq',
           side_effect=get_name_from_seq)
    def test_create_extracted_data(self, f_get_name):
        acc = func_prepare_acc()
        seqcs = [PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS),
                 PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1),
                 PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)]
        dto = BoxplotPTDto('Boxplot(s) for tests', [seqcs], short_names_dict)
        expected_dict = OrderedDict([('({})'.format(TestsIdData.test1_id), dict_for_test_13['results']),
                                     ('({}) data 1'.format(TestsIdData.test2_id), dict_for_test_14['data1']),
                                     ('({}) data 2'.format(TestsIdData.test3_id), dict_for_test_41['data2'])])
        expected_str = json.dumps(expected_dict)
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, deepcopy(seqcs))

        ret_ds_info, ret_data_for_drawer = self.extractor.create_extracted_data(acc, seqcs, dto)
        self.assertEqual(ds_info, ret_ds_info)

        self.assertEqual(dto.title, ret_data_for_drawer.title)
        self.assertEqual(expected_str, ret_data_for_drawer.json_data_str)

    @patch('charts.boxplot_per_test.boxplot_pt_extractor.BoxplotPTExtractor.get_name_from_seq',
           side_effect=get_name_from_seq)
    def test_create_extracted_data_skip_seq(self, f_get_name):
        acc = func_prepare_acc()
        seqcs = [PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS),
                 PValueSequence(TestsIdData.non_existing_test_id, PValuesFileType.DATA, 1)]
        dto = BoxplotPTDto('Boxplot(s) for tests', [seqcs], short_names_dict)
        expected_dict = {'({})'.format(TestsIdData.test1_id): dict_for_test_13['results']}
        expected_str = json.dumps(expected_dict)
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS,
                                 [PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)])

        ret_ds_info, ret_data_for_drawer = self.extractor.create_extracted_data(acc, seqcs, dto)
        self.assertEqual(ds_info, ret_ds_info)

        self.assertEqual(dto.title, ret_data_for_drawer.title)
        self.assertEqual(expected_str, ret_data_for_drawer.json_data_str)

    def test_create_extracted_data_returns_none(self):
        dto1 = PValuesDto(dict_for_test_13)
        dto2 = PValuesDto(dict_for_test_14)
        dto3 = PValuesDto(dict_for_test_41)
        dto4 = PValuesDto(dict_for_test_42)

        acc = PValuesAccumulator()
        acc.add(TestsIdData.test1_id, dto1)
        acc.add(TestsIdData.test2_id, dto2)
        acc.add(TestsIdData.test3_id, dto3)
        acc.add(TestsIdData.test4_id, dto4)
        seqcs = [PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS)]
        dto = BoxplotPTDto('Boxplot(s) for tests', [seqcs])

        ret = self.extractor.create_extracted_data(acc, seqcs, dto)
        self.assertIsNone(ret)

    def test_get_name_from_seq_results(self):
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        name = self.extractor.get_name_from_seq(seq, short_names_dict)
        expected = 'Frequency'.format(TestsIdData.test1_id)
        self.assertEqual(expected, name)

    def test_get_name_from_seq_data(self):
        seq = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        name = self.extractor.get_name_from_seq(seq, short_names_dict)
        expected = 'Cumulative Sums data 2'.format(TestsIdData.test2_id)
        self.assertEqual(expected, name)

    @patch('managers.nisttestmanager.NistTestManager.get_nist_param_for_test')
    def test_get_name_from_seq_special_param(self, f_get):
        nist_param = NistParam()
        nist_param.test_number = 2
        nist_param.special_parameter = 123
        f_get.return_value = nist_param
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        name = self.extractor.get_name_from_seq(seq, short_names_dict)
        expected = 'Block Frequency (123)'
        self.assertEqual(expected, name)

    @patch('managers.dbtestmanager.DBTestManager.get_test_by_id')
    def test_get_name_from_seq_throws(self, method_mock):
        test = Test()
        test.test_table = 'table'
        method_mock.return_value = test
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        with self.assertRaises(RuntimeError) as ex:
            self.extractor.get_name_from_seq(seq, short_names_dict)
        self.assertEqual('Unknown test type table', str(ex.exception))

    def test_get_p_values_results(self):
        acc = func_prepare_acc()
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        expected = dict_for_test_13['results']
        ret = self.extractor.get_p_values(acc, seq)
        self.assertEqual(expected, ret)

    def test_get_p_values_data(self):
        acc = func_prepare_acc()
        seq = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 1)
        expected = dict_for_test_41['data1']
        ret = self.extractor.get_p_values(acc, seq)
        self.assertEqual(expected, ret)

        seq = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)
        expected = dict_for_test_41['data2']
        ret = self.extractor.get_p_values(acc, seq)
        self.assertEqual(expected, ret)

    def test_get_p_values_not_in_acc(self):
        acc = func_prepare_acc()
        seq = PValueSequence(TestsIdData.non_existing_test_id, PValuesFileType.DATA, 1)
        ret = self.extractor.get_p_values(acc, seq)
        self.assertIsNone(ret)

    def test_get_p_values_unknown_file_type(self):
        acc = func_prepare_acc()
        seq = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)
        seq.p_values_file = -2
        with self.assertRaises(RuntimeError) as ex:
            self.extractor.get_p_values(acc, seq)
        self.assertTrue('Unknown test file type -2', str(ex.exception))
