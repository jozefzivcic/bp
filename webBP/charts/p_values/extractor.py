from charts.p_values_chart_dto import PValuesChartDto
from charts.p_values.data_for_p_values_drawer import DataForPValuesDrawer
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool
from managers.dbtestmanager import DBTestManager
from managers.nisttestmanager import NistTestManager
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto


class Extractor:
    threshold_is_zero = 1E-6

    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._test_dao = DBTestManager(pool)
        self._nist_dao = NistTestManager(pool)
        self._config_storage = storage
        self._i = 1

    def get_data_from_accumulator(self, acc: PValuesAccumulator, dto: PValuesChartDto) -> DataForPValuesDrawer:
        data = DataForPValuesDrawer()
        data.alpha = dto.alpha
        data.x_label = dto.x_label
        data.y_label = dto.y_label
        data.title = dto.title

        test_ids = acc.get_all_test_ids()
        self._i = 1

        for test_id in test_ids:
            p_values_dto = acc.get_dto_for_test(test_id)
            if p_values_dto.has_data_files():
                indices = p_values_dto.get_data_files_indices()
                for index in indices:
                    self.add_data(p_values_dto, data, test_id, index)
            else:
                self.add_data(p_values_dto, data, test_id)
        return data

    def add_data(self, dto: PValuesDto, data: DataForPValuesDrawer, test_id: int, index=None):
        if index is None:
            data.x_ticks_labels.append(self.get_test_name(test_id))
            p_values = dto.get_results_p_values()
        else:
            data.x_ticks_labels.append(self.get_test_name(test_id) + '_' + str(index))
            p_values = dto.get_data_p_values(index)

        data.x_ticks_positions.append(self._i)
        p_values = self.replace_zero_p_values(p_values)
        for p_value in p_values:
            data.x_values.append(self._i)
            data.y_values.append(p_value)
        self._i += 1

    def get_test_name(self, test_id: int):
        test = self._test_dao.get_test_by_id(test_id)
        if test.test_table == self._config_storage.nist:
            param = self._nist_dao.get_nist_param_for_test(test)
            return param.get_test_name()
        return 'Undefined'

    def replace_zero_p_values(self, p_values: list):
        return [Extractor.threshold_is_zero if x < Extractor.threshold_is_zero else x for x in p_values]
