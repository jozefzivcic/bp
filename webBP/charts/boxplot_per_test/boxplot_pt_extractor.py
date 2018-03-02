import json

from charts.boxplot_per_test.data_for_boxplot_pt_drawer import DataForBoxplotPTDrawer
from charts.boxplot_pt_dto import BoxplotPTDto
from charts.data_source_info import DataSourceInfo
from charts.extracted_data import ExtractedData
from charts.tests_in_chart import TestsInChart
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
        data_dict = {}
        seqcs = boxplot_dto.sequences
        for seq in seqcs:
            test_name = self.get_name_from_seq(seq)
            p_values = self.get_p_values(acc, seq)
            data_dict[test_name] = p_values
        json_str = json.dumps(data_dict)
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, seqcs)
        drawer_data = DataForBoxplotPTDrawer(boxplot_dto.title, json_str)
        return ExtractedData(ds_info, drawer_data)

    def get_name_from_seq(self, seq: PValueSequence) -> str:
        test = self._test_dao.get_test_by_id(seq.test_id)
        if test.test_table == self._config_storage.nist:
            test_name = self._nist_dao.get_nist_param_for_test(test).get_test_name()
        else:
            raise RuntimeError('Unknown test type {}'.format(test.test_table))
        if seq.p_values_file == PValuesFileType.DATA:
            test_name += ' data {}'.format(seq.data_num)
        return test_name

    def get_p_values(self, acc: PValuesAccumulator, seq: PValueSequence) -> list:
        dto = acc.get_dto_for_test(seq.test_id)
        if seq.p_values_file == PValuesFileType.RESULTS:
            return dto.get_results_p_values()
        elif seq.p_values_file == PValuesFileType.DATA:
            return dto.get_data_p_values(seq.data_num)
        else:
            raise RuntimeError('Unknown test file type {}'.format(seq.p_values_file))
