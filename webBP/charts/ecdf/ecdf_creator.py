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

    def create_ecdf_charts(self, data: DataForEcdfCreator):
        storage = ChartsStorage()
        data_list = self.extractor.get_data_from_accumulator(data.acc, data.ecdf_dto)
        for data in data_list:
            file_name = self.get_file_name(data.ds_info)
            self.drawer.draw_chart(data.data_for_drawer, file_name)

    def get_file_name(self, ds_info: DataSourceInfo):
        if ds_info.tests_in_chart != TestsInChart.SINGLE_TEST:
            raise ValueError('Expected single test, got {}.'.format(ds_info.tests_in_chart))
        seq = ds_info.p_value_sequence
        if seq.p_values_file == PValuesFileType.RESULTS:
            return 'ecdf_for_test{}_results.png'.format(seq.test_id)
        elif seq.p_values_file == PValuesFileType.DATA:
            return 'ecdf_for_test{}_data_{}.png'.format(seq.test_id, seq.data_num)
        else:
            raise ValueError('Unknown PValuesFileType {}'.format(seq.p_values_file))
