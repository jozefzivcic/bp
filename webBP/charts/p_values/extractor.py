from charts.extracted_data import ExtractedData
from charts.dto.p_values_chart_dto import PValuesChartDto
from charts.p_values.data_for_p_values_drawer import DataForPValuesDrawer
from common.helper_functions import filter_chart_x_ticks
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
        self._zoomed = False

    def get_data_from_accumulator(self, acc: PValuesAccumulator, chart_dto: PValuesChartDto) -> ExtractedData:
        data = DataForPValuesDrawer()
        data.alpha = chart_dto.alpha
        data.x_label = chart_dto.x_label
        data.y_label = chart_dto.y_label
        data.title = chart_dto.title
        data.zoomed = chart_dto.zoomed

        y_axis_ticks = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0]
        y_axis_labels = ['0.0', '0.00001', '0.0001', '0.001', '0.01', '0.1', '1.0']

        if not chart_dto.zoomed:
            data.y_axis_ticks = y_axis_ticks
            data.y_axis_labels = y_axis_labels
        else:
            self.set_y_axis(chart_dto.alpha, y_axis_ticks, y_axis_labels, data)
        test_ids = acc.get_all_test_ids()
        self._i = 1

        for test_id in test_ids:
            p_values_dto = acc.get_dto_for_test(test_id)
            if p_values_dto.has_data_files():
                indices = p_values_dto.get_data_files_indices()
                for index in indices:
                    self.add_data(chart_dto, p_values_dto, data, test_id, index)
            else:
                self.add_data(chart_dto, p_values_dto, data, test_id)
        self.filter_x_labels(data)
        ex_data = ExtractedData()
        ex_data.add_data(None, data)
        return ex_data

    def add_data(self, chart_dto: PValuesChartDto, dto: PValuesDto, data: DataForPValuesDrawer, test_id: int,
                 index=None):
        if index is None:
            data.x_ticks_labels.append(self.get_test_name(test_id, index, chart_dto.test_names))
            p_values = dto.get_results_p_values()
        else:
            data.x_ticks_labels.append(self.get_test_name(test_id, index, chart_dto.test_names))
            p_values = dto.get_data_p_values(index)

        data.x_ticks_positions.append(self._i)
        p_values = self.replace_zero_p_values(p_values)
        for p_value in p_values:
            if chart_dto.zoomed and p_value > chart_dto.alpha:
                continue
            data.x_values.append(self._i)
            data.y_values.append(p_value)
        self._i += 1

    def get_test_name(self, test_id: int, index: int, test_names: dict) -> str:
        test = self._test_dao.get_test_by_id(test_id)
        if test.test_table != self._config_storage.nist:
            raise RuntimeError('Unsupported test table "{}"'.format(test.test_table))
        param = self._nist_dao.get_nist_param_for_test(test)
        test_type = param.get_test_type()
        test_name = test_names.get(test_type)
        if index is not None:
            test_name += ' data {}'.format(index)
        if param.has_special_parameter():
            test_name += ' ({})'.format(param.special_parameter)
        return test_name

    def replace_zero_p_values(self, p_values: list):
        return [Extractor.threshold_is_zero if x < Extractor.threshold_is_zero else x for x in p_values]

    def set_y_axis(self, alpha, y_axis_ticks: list, y_axis_labels: list, data: DataForPValuesDrawer):
        l = len(y_axis_ticks)
        temp_ticks = [0.000001]
        temp_labels = ['0.0']
        if alpha <= 0.000001:
            temp_ticks.append(0.00001)
            temp_labels.append('0.00001')
            data.y_axis_ticks = temp_ticks
            data.y_axis_labels = temp_labels
            return

        for i in range(1, l):
            if y_axis_ticks[i] < alpha:
                temp_ticks.append(y_axis_ticks[i])
                temp_labels.append(y_axis_labels[i])
            else:
                break
        temp_ticks.append(alpha)
        temp_labels.append(('%.6f' % alpha).rstrip('0').rstrip('.'))
        data.y_axis_ticks = temp_ticks
        data.y_axis_labels = temp_labels

    def filter_x_labels(self, data: DataForPValuesDrawer):
        x_ticks_pos = data.x_ticks_positions
        x_ticks_labels = data.x_ticks_labels
        x_ticks_pos_f, x_ticks_labels_f = filter_chart_x_ticks(x_ticks_pos, x_ticks_labels)
        data.x_ticks_positions = x_ticks_pos_f
        data.x_ticks_labels = x_ticks_labels_f
