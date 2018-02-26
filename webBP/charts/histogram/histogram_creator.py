from os.path import join

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.histogram.data_for_histogram_creator import DataForHistogramCreator
from charts.histogram.histogram_drawer import HistogramDrawer
from charts.histogram.historam_extractor import HistogramExtractor


class HistogramCreator:
    def __init__(self):
        self._extractor = HistogramExtractor()
        self.drawer = HistogramDrawer()

    def create_histogram(self, data: DataForHistogramCreator) -> ChartInfo:
        self.check_input(data)
        file = self.get_file_name_for_chart(data.directory, data.file_id)
        extracted_data = self._extractor.get_data_from_accumulator(data.acc, data.histogram_dto)
        self.drawer.draw_chart(extracted_data.data_for_drawer, file)
        return ChartInfo(extracted_data.ds_info, file, ChartType.HISTOGRAM, data.file_id)

    def get_file_name_for_chart(self, directory, file_id):
        file_name = 'histogram_for_file_' + str(file_id) + '.png'
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
