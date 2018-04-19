import math

from charts.dto.proportions_dto import ProportionsDto
from charts.extracted_data import ExtractedData
from charts.proportions.data_for_proportions_drawer import DataForProportionsDrawer
from charts.different_num_of_pvals_error import DifferentNumOfPValsError
from common.error.diff_pvalues_len_err import DiffPValuesLenErr
from common.helper_functions import filter_chart_x_ticks
from configstorage import ConfigStorage
from enums.prop_formula import PropFormula
from managers.connectionpool import ConnectionPool
from managers.dbtestmanager import DBTestManager
from managers.nisttestmanager import NistTestManager
from p_value_processing.p_values_accumulator import PValuesAccumulator


class ProportionsExtractor(object):
    zero_threshold = 0.000000

    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._test_dao = DBTestManager(pool)
        self._nist_dao = NistTestManager(pool)
        self._config_storage = storage

    def get_data_from_accumulator(self, acc: PValuesAccumulator, prop_dto: ProportionsDto) -> ExtractedData:
        ex_data = ExtractedData()
        test_ids = acc.get_all_test_ids()
        test = self._test_dao.get_test_by_id(test_ids[0])
        num_of_seqcs = self._nist_dao.get_nist_param_for_test(test).streams
        low, mid, high = self.get_interval(prop_dto.formula, prop_dto.alpha, num_of_seqcs)
        limit_low = max(low - 0.2, 0.0)
        limit_high = min(high + 0.2, 1.0)

        try:
            x_ticks, y_values = self.process_p_vals(acc, prop_dto, num_of_seqcs)
        except DifferentNumOfPValsError as ex:
            err = DiffPValuesLenErr(ex.expected_len, ex.actual_len)
            ex_data.add_err(err)
            return ex_data

        x_ticks_pos = list(range(0, len(x_ticks)))
        x_values = list(x_ticks_pos)
        x_ticks_pos, x_ticks = self.filter_x_ticks(x_ticks_pos, x_ticks)
        data_drawer = DataForProportionsDrawer(prop_dto.title, prop_dto.x_label, prop_dto.y_label, limit_low,
                                               limit_high, x_ticks_pos, x_ticks, x_values, y_values, low, high, mid)
        ex_data.add_data(None, data_drawer)
        return ex_data

    def process_p_vals(self, acc: PValuesAccumulator, prop_dto: ProportionsDto, num_of_seqcs: int):
        test_ids = acc.get_all_test_ids()
        x_ticks = []
        y_values = []
        for test_id in test_ids:
            dto = acc.get_dto_for_test(test_id)
            if dto.has_data_files():
                for data_num in dto.get_data_files_indices():
                    p_values = dto.get_data_p_values(data_num)
                    proportions = self.get_proportions(p_values, prop_dto.alpha, num_of_seqcs)
                    test_name = self.get_test_name(prop_dto.test_names, test_id, data_num)
                    x_ticks.append(test_name)
                    y_values.append(proportions)
            else:
                p_values = dto.get_results_p_values()
                proportions = self.get_proportions(p_values, prop_dto.alpha, num_of_seqcs)
                test_name = self.get_test_name(prop_dto.test_names, test_id)
                x_ticks.append(test_name)
                y_values.append(proportions)
        return x_ticks, y_values

    def get_proportions(self, p_values: list, alpha: float, exp_len: int) -> float:
        if exp_len != len(p_values):
            raise DifferentNumOfPValsError('Number of p_values in file is different than given as a parameter streams.'
                                           ' ({}, {})'.format(len(p_values), exp_len), exp_len, len(p_values))
        sample_size = 0
        count = 0
        for p in p_values:
            if p > ProportionsExtractor.zero_threshold:
                sample_size += 1
                if p < alpha:
                    count += 1
        if sample_size == 0:
            return 0.0
        return 1.0 - float(count) / float(sample_size)

    def get_interval(self, formula: PropFormula, alpha: float, num_of_seqcs: float) -> tuple:
        if formula == PropFormula.ORIGINAL:
            mid = 1.0 - alpha
            side = 3.0 * math.sqrt((alpha * (1.0 - alpha)) / float(num_of_seqcs))
            return mid - side, mid, mid + side
        elif formula == PropFormula.IMPROVED:
            mid = 1.0 - alpha
            side = 2.6 * math.sqrt((alpha * (1.0 - alpha)) / float(num_of_seqcs))
            return mid - side, mid, mid + side
        else:
            raise RuntimeError('Unsupported type of formula: "{}"'.format(formula))

    def get_test_name(self, test_names: dict, test_id: int, data_num: int=None) -> str:
        test = self._test_dao.get_test_by_id(test_id)
        if test.test_table != self._config_storage.nist:
            raise RuntimeError('Undefined table "{}" for test_id: {}. Expected "nist" as test table'
                               .format(test.test_table, test_id))
        nist_param = self._nist_dao.get_nist_param_for_test(test)
        test_type = nist_param.get_test_type()
        test_name = test_names.get(test_type)
        if data_num is not None:
            test_name += ' data {}'.format(data_num)
        if nist_param.has_special_parameter():
            test_name += ' ({})'.format(nist_param.special_parameter)
        return test_name

    def filter_x_ticks(self, x_ticks_pos: list, x_ticks: list) -> tuple:
        return filter_chart_x_ticks(x_ticks_pos, x_ticks)
