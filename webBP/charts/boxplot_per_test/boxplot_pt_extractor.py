import json

from charts.boxplot_per_test.data_for_boxplot_pt_drawer import DataForBoxplotPTDrawer
from charts.different_num_of_pvals_error import DifferentNumOfPValsError
from charts.dto.boxplot_pt_dto import BoxplotPTDto
from charts.data_source_info import DataSourceInfo
from charts.extracted_data import ExtractedData
from charts.tests_in_chart import TestsInChart
from common.error.diff_pvalues_len_err import DiffPValuesLenErr
from common.helper_functions import list_difference
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool
from managers.dbtestmanager import DBTestManager
from managers.nisttestmanager import NistTestManager
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_file_type import PValuesFileType


class BoxplotPTExtractor:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._test_dao = DBTestManager(pool)
        self._nist_dao = NistTestManager(pool)
        self._config_storage = storage

    def get_data_from_accumulator(self, acc: PValuesAccumulator, boxplot_dto: BoxplotPTDto) -> ExtractedData:
        seqcs_all_charts = boxplot_dto.sequences
        extracted_data = ExtractedData()
        for seqcs_for_chart in seqcs_all_charts:
            try:
                ret = self.create_extracted_data(acc, seqcs_for_chart, boxplot_dto)
            except DifferentNumOfPValsError as ex:
                err = DiffPValuesLenErr(ex.expected_len, ex.actual_len)
                extracted_data.add_err(err)
                return extracted_data
            if ret is None:
                continue
            extracted_data.add_data(ret[0], ret[1])
        return extracted_data

    def create_extracted_data(self, acc: PValuesAccumulator, seqcs: list, boxplot_dto: BoxplotPTDto) -> tuple:
        data_dict = {}
        seqcs_not_used = []
        test = self._test_dao.get_test_by_id(seqcs[0].test_id)
        expected_streams = self._nist_dao.get_nist_param_for_test(test).streams
        for seq in seqcs:
            p_values = self.get_p_values(acc, seq)
            if p_values is None:
                seqcs_not_used.append(seq)
                continue
            if expected_streams != len(p_values):
                raise DifferentNumOfPValsError('Expected {} p-values, found only {}.'
                                               .format(expected_streams, len(p_values)), expected_streams,
                                               len(p_values))
            test_name = self.get_name_from_seq(seq, boxplot_dto.test_names)
            data_dict[test_name] = p_values
        if not data_dict:
            return None
        json_str = json.dumps(data_dict)
        res_seqcs = list_difference(seqcs, seqcs_not_used)
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, res_seqcs)
        drawer_data = DataForBoxplotPTDrawer(boxplot_dto.title, json_str)
        return ds_info, drawer_data

    def get_name_from_seq(self, seq: PValueSequence, test_names) -> str:
        test = self._test_dao.get_test_by_id(seq.test_id)
        if test.test_table != self._config_storage.nist:
            raise RuntimeError('Unknown test type {}'.format(test.test_table))
        nist_param = self._nist_dao.get_nist_param_for_test(test)
        test_type = nist_param.get_test_type()
        test_name = test_names.get(test_type)
        if seq.p_values_file == PValuesFileType.DATA:
            test_name += ' data {}'.format(seq.data_num)
        if nist_param.has_special_parameter():
            test_name += ' ({})'.format(nist_param.special_parameter)
        return test_name

    def get_p_values(self, acc: PValuesAccumulator, seq: PValueSequence) -> list:
        dto = acc.get_dto_for_test_safe(seq.test_id)
        if dto is None:
            return None
        if seq.p_values_file == PValuesFileType.RESULTS:
            return dto.get_results_p_values()
        elif seq.p_values_file == PValuesFileType.DATA:
            return dto.get_data_p_values(seq.data_num)
        else:
            raise RuntimeError('Unknown test file type {}'.format(seq.p_values_file))
