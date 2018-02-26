import common.helper_functions
from charts.data_source_info import DataSourceInfo
from charts.extracted_data import ExtractedData
from charts.test_dependency.data_for_test_dependency_drawer import DataForTestDependencyDrawer
from charts.test_dependency_dto import TestDependencyDto
from charts.tests_in_chart import TestsInChart
from configstorage import ConfigStorage
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

    def get_data_from_accumulator(self, acc: PValuesAccumulator, dto: TestDependencyDto) -> list:
        seq_pairs = dto.seq_accumulator.generate_sequence_pairs(acc)
        seq_pairs.filter_pairs(common.helper_functions.check_for_uniformity)
        tuples = seq_pairs.get_pairs_in_list()
        data_for_drawer_list = []
        for seq1, seq2, p_values1, p_values2 in tuples:
            name1 = self.get_test_name(seq1)
            name2 = self.get_test_name(seq2)
            data_for_drawer = DataForTestDependencyDrawer(p_values1, p_values2, dto.title, name1, name2)
            ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
            extracted_data = ExtractedData(ds_info, data_for_drawer)
            data_for_drawer_list.append(extracted_data)
        return data_for_drawer_list

    def get_test_name(self, seq: PValueSequence):
        test = self._test_dao.get_test_by_id(seq.test_id)
        if test.test_table == self._config_storage.nist:
            test_name = self._nist_dao.get_nist_param_for_test(test).get_test_name()
            if seq.p_values_file == PValuesFileType.DATA:
                test_name += '_data_' + str(seq.data_num)
            return test_name
        raise RuntimeError('Unsupported test type ' + str(test.test_table))
