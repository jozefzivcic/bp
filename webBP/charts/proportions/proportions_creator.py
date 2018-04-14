from os.path import join

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.proportions.data_for_proportions_creator import DatForProportionsCreator
from charts.proportions.proportions_drawer import ProportionsDrawer
from charts.proportions.proportions_extractor import ProportionsExtractor
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool
from p_value_processing.p_values_accumulator import PValuesAccumulator


class ProportionsCreator(object):
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._extractor = ProportionsExtractor(pool, storage)
        self._drawer = ProportionsDrawer()

    def create_prop_chart(self, data: DatForProportionsCreator) -> ChartsStorage:
        storage = ChartsStorage()
        ex_data = self._extractor.get_data_from_accumulator(data.acc, data.prop_dto)
        ex_data_list = ex_data.get_all_data()
        for ds_info, data_for_drawer, info, err in ex_data_list:
            file_name = self.get_file_name(data.directory, data.acc)
            self._drawer.draw_chart(data_for_drawer, file_name)
            chart_info = ChartInfo(ds_info, file_name, ChartType.PROPORTIONS, data.file_id)
            storage.add_chart_info(chart_info, info, err)
        storage.add_infos_from_chart(ChartType.PROPORTIONS, ex_data.get_all_infos())
        storage.add_errors_from_chart(ChartType.TESTS_DEPENDENCY, ex_data.get_all_errs())
        return storage

    def get_file_name(self, directory: str, acc: PValuesAccumulator):
        file_name = 'prop_first_test_id_{}.png'.format(acc.get_all_test_ids()[0])
        return join(directory, file_name)
