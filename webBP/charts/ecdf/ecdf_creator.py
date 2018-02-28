from os.path import join

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.data_source_info import DataSourceInfo
from charts.ecdf.data_for_ecdf_creator import DataForEcdfCreator
from charts.ecdf.ecdf_drawer import EcdfDrawer
from charts.ecdf.ecdf_extractor import EcdfExtractor
from charts.tests_in_chart import TestsInChart
from p_value_processing.p_values_file_type import PValuesFileType


class EcdfCreator:
    def __init__(self):
        self.drawer = EcdfDrawer()
        self.extractor = EcdfExtractor()

    def create_ecdf_charts(self, data_for_creator: DataForEcdfCreator) -> ChartsStorage:
        storage = ChartsStorage()
        data_list = self.extractor.get_data_from_accumulator(data_for_creator.acc, data_for_creator.ecdf_dto)
        for data in data_list:
            file_name = self.get_file_name(data.ds_info, data_for_creator.directory)
            self.drawer.draw_chart(data.data_for_drawer, file_name)
            chart_info = ChartInfo(data.ds_info, file_name, ChartType.ECDF, data_for_creator.file_id)
            storage.add_chart_info(chart_info)
        return storage

    def get_file_name(self, ds_info: DataSourceInfo, directory):
        if ds_info.tests_in_chart != TestsInChart.SINGLE_TEST:
            raise ValueError('Expected single test, got {}.'.format(ds_info.tests_in_chart))
        seq = ds_info.p_value_sequence
        if seq.p_values_file == PValuesFileType.RESULTS:
            name = 'ecdf_for_test_{}_results.png'.format(seq.test_id)
            return join(directory, name)
        elif seq.p_values_file == PValuesFileType.DATA:
            name = 'ecdf_for_test_{}_data_{}.png'.format(seq.test_id, seq.data_num)
            return join(directory, name)
        else:
            raise ValueError('Unknown PValuesFileType {}'.format(seq.p_values_file))
