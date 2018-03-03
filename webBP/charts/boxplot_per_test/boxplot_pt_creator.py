from os.path import join

from charts.boxplot_per_test.boxplot_pt_drawer import BoxplotPTDrawer
from charts.boxplot_per_test.boxplot_pt_extractor import BoxplotPTExtractor
from charts.boxplot_per_test.data_for_boxplot_pt_creator import DataForBoxplotPTCreator
from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool


class BoxplotPTCreator:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._drawer = BoxplotPTDrawer()
        self._extractor = BoxplotPTExtractor(pool, storage)

    def create_boxplots(self, data: DataForBoxplotPTCreator) -> ChartsStorage:
        storage = ChartsStorage()
        extracted_data_list = self._extractor.get_data_from_accumulator(data.acc, data.dto)
        for i, extracted_data in enumerate(extracted_data_list):
            file_name = self.get_filename(data.directory, i)
            self._drawer.draw_chart(extracted_data.data_for_drawer, file_name)
            ch_info = ChartInfo(extracted_data.ds_info, file_name, ChartType.BOXPLOT_PT, data.file_id)
            storage.add_chart_info(ch_info)
        return storage

    def get_filename(self, directory: str, i: int) -> str:
        name = 'boxplot_pt_{}.png'.format(i)
        return join(directory, name)
