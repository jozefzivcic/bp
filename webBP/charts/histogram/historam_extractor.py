import json
import math

from charts.data_source_info import DataSourceInfo
from charts.extracted_data import ExtractedData
from charts.histogram.data_for_histogram_drawer import DataForHistogramDrawer
from charts.dto.histogram_dto import HistogramDto
from charts.tests_in_chart import TestsInChart
from enums.hist_for_tests import HistForTests
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_file_type import PValuesFileType


class HistogramExtractor:
    intervals = ['[0.0, 0.1)', '[0.1, 0.2)', '[0.2, 0.3)', '[0.3, 0.4)', '[0.4, 0.5)', '[0.5, 0.6)', '[0.6, 0.7)',
                 '[0.7, 0.8)', '[0.8, 0.9)', '[0.9, 1.0]']

    def get_data_from_accumulator(self, acc: PValuesAccumulator, dto: HistogramDto) -> ExtractedData:
        ex_data = ExtractedData()
        acc_quantities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for test_id in acc.get_all_test_ids():
            p_values_dto = acc.get_dto_for_test(test_id)
            if p_values_dto.has_data_files():
                for data_num in p_values_dto.get_data_files_indices():
                    self.add_data(ex_data, acc_quantities, p_values_dto.get_data_p_values(data_num), dto, test_id,
                                  data_num)
            else:
                self.add_data(ex_data, acc_quantities, p_values_dto.get_results_p_values(), dto, test_id)
        if not HistForTests.ALL_TESTS in dto.hist_for_tests:
            return ex_data
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, acc.get_all_test_ids())
        intervals_quantities = self.add_intervals_to_quantities(acc_quantities)
        intervals_quantities_str = json.dumps(intervals_quantities)
        data = DataForHistogramDrawer(intervals_quantities_str, dto.x_label, dto.y_label, dto.title)
        ex_data.add_data(ds_info, data)
        return ex_data

    def add_data(self, ex_data: ExtractedData, global_quantities: list, p_values: list, dto: HistogramDto,
                 test_id: int, data_num: int=None):
        quantities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.add_p_values_to_interval(quantities, p_values)
        if HistForTests.ALL_TESTS in dto.hist_for_tests:
            self.sum_quantities(global_quantities, quantities)
        if not HistForTests.INDIVIDUAL_TESTS in dto.hist_for_tests:
            return
        if data_num is None:
            seq = PValueSequence(test_id, PValuesFileType.RESULTS)
        else:
            seq = PValueSequence(test_id, PValuesFileType.DATA, data_num)
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, seq)
        intervals_quantities = self.add_intervals_to_quantities(quantities)
        intervals_quantities_str = json.dumps(intervals_quantities)
        data = DataForHistogramDrawer(intervals_quantities_str, dto.x_label, dto.y_label, dto.title)
        ex_data.add_data(ds_info, data)

    def add_p_values_to_interval(self, quantities: list, p_values: list):
        for p_value in p_values:
            pos = int(math.floor(p_value * 10))
            if pos >= 10:
                pos -= 1
            quantities[pos] += 1

    def add_intervals_to_quantities(self, quantities: list) -> list:
        ret = []
        for i in range(10):
            ret.append([HistogramExtractor.intervals[i], quantities[i]])
        return ret

    def sum_quantities(self, q1: list, q2: list) -> list:
        if len(q1) != len(q2):
            raise RuntimeError('Quantities do not have the same length ({}, {})'.format(len(q1), len(q2)))
        for i, quantity in enumerate(q2):
            q1[i] += quantity
