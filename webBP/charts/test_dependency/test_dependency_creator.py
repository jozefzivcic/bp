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
        arr_of_data = self._extractor.get_data_from_accumulator(data.acc, data.test_dependency_dto)
        for data_for_drawer in arr_of_data:
            file_name = self.get_file_name(data.directory, data_for_drawer)
            self._drawer.draw_chart(data_for_drawer, file_name)
            chart_info = ChartInfo(file_name, ChartType.TESTS_DEPENDENCY, data.file_id)
            storage.add_chart_info(chart_info)
        return storage

    def check_input(self, data: DataForTestDependencyCreator):
        if data is None:
            raise TypeError('Input data is None')

    def get_file_name(self, directory: str, data: DataForTestDependencyDrawer):
        file_name = 'dependency_of_' + data.x_label + '_and_' + data.y_label + '.png'
        file_name = file_name.replace(' ', '_')
        return join(directory, file_name)
