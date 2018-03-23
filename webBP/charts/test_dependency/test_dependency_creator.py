from os.path import join

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.test_dependency.data_for_test_dependency_creator import DataForTestDependencyCreator
from charts.test_dependency.data_for_test_dependency_drawer import DataForTestDependencyDrawer
from charts.test_dependency.test_dependency_drawer import TestDependencyDrawer
from charts.test_dependency.test_dependency_extractor import TestDependencyExtractor
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool


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
            file_name = self.get_file_name(data.directory, data_for_drawer)
            self._drawer.draw_chart(data_for_drawer, file_name)
            chart_info = ChartInfo(ds_info, file_name, ChartType.TESTS_DEPENDENCY, data.file_id)
            storage.add_chart_info(chart_info, info, err)
        storage.add_infos_from_chart(ChartType.TESTS_DEPENDENCY, extracted_data.get_all_infos())
        storage.add_errors_from_chart(ChartType.TESTS_DEPENDENCY, extracted_data.get_all_errs())
        return storage

    def check_input(self, data: DataForTestDependencyCreator):
        if data is None:
            raise TypeError('Input data is None')

    def get_file_name(self, directory: str, data: DataForTestDependencyDrawer):
        file_name = 'dependency_of_' + data.x_label + '_and_' + data.y_label + '.png'
        file_name = file_name.replace(' ', '_')
        return join(directory, file_name)
