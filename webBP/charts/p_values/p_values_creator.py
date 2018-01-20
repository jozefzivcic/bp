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

        file = self.get_file_name_for_p_values_chart(data.directory, data.file_id)
        data_for_chart = self._extractor.get_data_from_accumulator(data.acc, data.chart_options)
        self._p_values_drawer.draw_chart(data_for_chart, file)

        return ChartInfo(file, ChartType.P_VALUES, data.file_id)

    def get_file_name_for_p_values_chart(self, directory, file_id):
        file_name = 'p_values_for_file_' + str(file_id) + '.png'
        return join(directory, file_name)