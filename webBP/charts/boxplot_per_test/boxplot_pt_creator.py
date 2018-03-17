from os.path import join

from charts.boxplot_per_test.boxplot_pt_drawer import BoxplotPTDrawer
from charts.boxplot_per_test.boxplot_pt_extractor import BoxplotPTExtractor
from charts.boxplot_per_test.data_for_boxplot_pt_creator import DataForBoxplotPTCreator
from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.data_source_info import DataSourceInfo
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool


class BoxplotPTCreator:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._drawer = BoxplotPTDrawer()
        self._extractor = BoxplotPTExtractor(pool, storage)

    def create_boxplots(self, data: DataForBoxplotPTCreator) -> ChartsStorage:
        storage = ChartsStorage()
        extracted_data = self._extractor.get_data_from_accumulator(data.acc, data.dto)
        for ds_info, data_for_drawer, info, err in extracted_data.get_all_data():
            file_name = self.get_filename(data.directory, ds_info)
            self._drawer.draw_chart(data_for_drawer, file_name)
            ch_info = ChartInfo(ds_info, file_name, ChartType.BOXPLOT_PT, data.file_id)
            storage.add_chart_info(ch_info)
        return storage

    def get_filename(self, directory: str, info: DataSourceInfo) -> str:
        first_test = info.p_value_sequence[0].test_id
        name = 'boxplot_pt_{}.png'.format(first_test)
        return join(directory, name)
