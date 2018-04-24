from os.path import join

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.data_source_info import DataSourceInfo
from charts.histogram.data_for_histogram_creator import DataForHistogramCreator
from charts.histogram.histogram_drawer import HistogramDrawer
from charts.histogram.historam_extractor import HistogramExtractor
from charts.tests_in_chart import TestsInChart
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType


class HistogramCreator:
    def __init__(self):
        self._extractor = HistogramExtractor()
        self._drawer = HistogramDrawer()

    def create_histogram(self, data: DataForHistogramCreator) -> ChartsStorage:
        self.check_input(data)
        storage = ChartsStorage()
        extracted_data = self._extractor.get_data_from_accumulator(data.acc, data.histogram_dto)
        ex_data_list = extracted_data.get_all_data()
        for ds_info, data_for_drawer, info, err in ex_data_list:
            file_name = self.get_file_name_for_chart(data.directory, ds_info)
            self._drawer.draw_chart(data_for_drawer, file_name)
            ch_info = ChartInfo(ds_info, file_name, ChartType.HISTOGRAM, data.file_id)
            storage.add_chart_info(ch_info, info, err)
        storage.add_infos_from_chart(ChartType.HISTOGRAM, extracted_data.get_all_infos())
        storage.add_errors_from_chart(ChartType.HISTOGRAM, extracted_data.get_all_errs())
        return storage

    def get_file_name_for_chart(self, directory: str, ds_info: DataSourceInfo):
        if ds_info.tests_in_chart == TestsInChart.MULTIPLE_TESTS:
            file_name = 'hist_mult_t_first_tid_{}.png'.format(ds_info.p_value_sequence[0].test_id)
            return join(directory, file_name)
        seq = ds_info.p_value_sequence  # type: PValueSequence
        seq_str = 't{}'.format(seq.test_id)
        if seq.p_values_file == PValuesFileType.DATA:
            seq_str += '_data{}'.format(seq.data_num)
        file_name = 'hist_single_{}'.format(seq_str)
        return join(directory, file_name)

    def check_input(self, data: DataForHistogramCreator):
        if data is None:
            raise TypeError('Data is None')
        if data.histogram_dto is None:
            raise TypeError('Histogram DTO is None')
        if data.acc is None:
            raise TypeError('Accumulator is None')
        if data.directory is None:
            raise TypeError('Directory is None')
        if data.file_id is None:
            raise TypeError('File id is None')
