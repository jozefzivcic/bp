from charts.boxplot_per_test.boxplot_pt_drawer import BoxplotPTDrawer
from charts.boxplot_per_test.boxplot_pt_extractor import BoxplotPTExtractor
from charts.boxplot_per_test.data_for_boxplot_pt_creator import DataForBoxplotPTCreator
from charts.boxplot_pt_dto import BoxplotPTDto
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
            file_name = self.get_filename(data.dto)
            self._drawer.draw_chart(extracted_data, file_name)
            ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, data.dto.sequences[i])
            ch_info = ChartInfo(ds_info, file_name, ChartType.BOXPLOT_PT, data.file_id)
            storage.add_chart_info(ch_info)
        return storage

    def get_filename(self, dto: BoxplotPTDto) -> str:
        return ''



