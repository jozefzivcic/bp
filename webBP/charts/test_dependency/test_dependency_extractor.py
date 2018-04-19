from charts.data_source_info import DataSourceInfo
from charts.dto.test_dependency_dto import TestDependencyDto
from charts.extracted_data import ExtractedData
from charts.test_dependency.data_for_test_dependency_drawer import DataForTestDependencyDrawer
from charts.tests_in_chart import TestsInChart
from p_value_processing.different_lists_size_error import DifferentListsSizeError
from common.error.test_dep_seq_len_err import TestDepSeqLenErr
from common.info.test_dep_filtered_info import TestDepFilteredInfo
from common.info.test_dep_unif_info import TestDepUnifInfo
from common.unif_check import UnifCheck
from configstorage import ConfigStorage
from enums.filter_uniformity import FilterUniformity
from managers.connectionpool import ConnectionPool
from managers.dbtestmanager import DBTestManager
from managers.nisttestmanager import NistTestManager
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_file_type import PValuesFileType


class TestDependencyExtractor:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._test_dao = DBTestManager(pool)
        self._nist_dao = NistTestManager(pool)
        self._config_storage = storage

    def get_data_from_accumulator(self, acc: PValuesAccumulator, dto: TestDependencyDto) -> ExtractedData:
        extracted_data = ExtractedData()
        seq_pairs = dto.seq_accumulator.generate_sequence_pairs(acc, dto.pairs)
        unif_check = UnifCheck(dto.alpha, 5)
        try:
            data = seq_pairs.filter_pairs(unif_check, dto.filter_unif)
        except DifferentListsSizeError as ex:
            error = TestDepSeqLenErr(ex.seq1, ex.len1, ex.seq2, ex.len2)
            extracted_data.add_err(error)
            return extracted_data

        tuples = seq_pairs.get_pairs_in_list()
        for seq1, seq2, p_values1, p_values2 in tuples:
            name1 = self.get_test_name(seq1, dto.test_names)
            name2 = self.get_test_name(seq2, dto.test_names)
            item_dto = data.get_kept_by_seqcs(seq1, seq2)
            data_for_drawer = DataForTestDependencyDrawer(p_values1, p_values2, dto.title, name1, name2)
            ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
            info = TestDepUnifInfo(item_dto.p_value, item_dto.condition_fulfilled)
            extracted_data.add_data(ds_info, data_for_drawer, info)
        len_kept = data.get_kept_len()
        len_deleted = data.get_deleted_len()
        if dto.filter_unif != FilterUniformity.DO_NOT_FILTER:
            info = TestDepFilteredInfo(len_deleted, len_kept + len_deleted, dto.filter_unif)
            extracted_data.add_info(info)
        return extracted_data

    def get_test_name(self, seq: PValueSequence, test_names: dict):
        test = self._test_dao.get_test_by_id(seq.test_id)
        if test.test_table != self._config_storage.nist:
            raise RuntimeError('Unsupported test type ' + str(test.test_table))
        param = self._nist_dao.get_nist_param_for_test(test)
        test_type = param.get_test_type()
        test_name = test_names.get(test_type)
        if seq.p_values_file == PValuesFileType.DATA:
            test_name += ' data {}'.format(seq.data_num)
        if param.has_special_parameter():
            test_name += ' ({})'.format(param.special_parameter)
        return test_name
