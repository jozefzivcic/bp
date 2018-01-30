from os.path import join

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.p_values.data_for_p_values_creator import DataForPValuesCreator
from charts.p_values.extractor import Extractor
from charts.p_values.p_values_drawer import PValuesDrawer
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool


class PValuesCreator:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._extractor = Extractor(pool, storage)
        self._p_values_drawer = PValuesDrawer()

    def create_p_values_chart(self, data: DataForPValuesCreator) -> ChartInfo:
        if data is None:
            raise TypeError('Data cannot be None')
        if data.chart_options is None:
            raise TypeError('Chart options cannot be None')
        if data.acc is None:
            raise TypeError('Accumulator cannot be None')
        if data.directory is None:
            raise TypeError('Directory cannot be None')
        if data.file_id is None:
            raise TypeError('file_id cannot be None')

        file = self.get_file_name_for_p_values_chart(data)
        data_for_chart = self._extractor.get_data_from_accumulator(data.acc, data.chart_options)
        self._p_values_drawer.draw_chart(data_for_chart, file)

        chart_type = ChartType.P_VALUES_ZOOMED if data.chart_options.zoomed else ChartType.P_VALUES
        return ChartInfo(file, chart_type, data.file_id)

    def get_file_name_for_p_values_chart(self, data: DataForPValuesCreator):
        zoomed_str = '_zoomed' if data.chart_options.zoomed else ''
        file_name = 'p_values_for_file_' + str(data.file_id) + zoomed_str + '.png'
        return join(data.directory, file_name)
