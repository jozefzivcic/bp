from os.path import join

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.data_source_info import DataSourceInfo
from charts.test_dependency.data_for_test_dependency_creator import DataForTestDependencyCreator
from charts.test_dependency.test_dependency_drawer import TestDependencyDrawer
from charts.test_dependency.test_dependency_extractor import TestDependencyExtractor
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType


class TestDependencyCreator:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._extractor = TestDependencyExtractor(pool, storage)
        self._drawer = TestDependencyDrawer()

    def create_test_dependency_charts(self, data: DataForTestDependencyCreator) -> ChartsStorage:
        self.check_input(data)
        storage = ChartsStorage()
        extracted_data = self._extractor.get_data_from_accumulator(data.acc, data.test_dependency_dto)
        ex_data_list = extracted_data.get_all_data()
        for ds_info, data_for_drawer, info, err in ex_data_list:
            file_name = self.get_file_name(data.directory, ds_info)
            self._drawer.draw_chart(data_for_drawer, file_name)
            chart_info = ChartInfo(ds_info, file_name, ChartType.TESTS_DEPENDENCY, data.file_id)
            storage.add_chart_info(chart_info, info, err)
        storage.add_infos_from_chart(ChartType.TESTS_DEPENDENCY, extracted_data.get_all_infos())
        storage.add_errors_from_chart(ChartType.TESTS_DEPENDENCY, extracted_data.get_all_errs())
        return storage

    def check_input(self, data: DataForTestDependencyCreator):
        if data is None:
            raise TypeError('Input data is None')

    def get_file_name(self, directory: str, ds_info: DataSourceInfo) -> str:
        seq1 = ds_info.p_value_sequence[0]  # type: PValueSequence
        seq2 = ds_info.p_value_sequence[1]  # type: PValueSequence
        seq1_str = self.get_seq_str(seq1)
        seq2_str = self.get_seq_str(seq2)
        file_name = 'dependency_of_{}_and_{}.png'.format(seq1_str, seq2_str)
        return join(directory, file_name)

    def get_seq_str(self, seq: PValueSequence) -> str:
        if seq.p_values_file == PValuesFileType.RESULTS:
            return '{}_res'.format(seq.test_id)
        elif seq.p_values_file == PValuesFileType.DATA:
            return '{}_data{}'.format(seq.test_id, seq.data_num)
        else:
            raise RuntimeError('Unsupported file type {}'.format(seq.p_values_file))
