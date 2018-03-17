import json
import math

from charts.extracted_data import ExtractedData
from charts.histogram.data_for_histogram_drawer import DataForHistogramDrawer
from charts.dto.histogram_dto import HistogramDto
from p_value_processing.p_values_accumulator import PValuesAccumulator


class HistogramExtractor:
    intervals = ['[0.0, 0.1)', '[0.1, 0.2)', '[0.2, 0.3)', '[0.3, 0.4)', '[0.4, 0.5)', '[0.5, 0.6)', '[0.6, 0.7)',
                 '[0.7, 0.8)', '[0.8, 0.9)', '[0.9, 1.0]']

    def get_data_from_accumulator(self, acc: PValuesAccumulator, dto: HistogramDto) -> ExtractedData:
        data = DataForHistogramDrawer()
        data.x_label = dto.x_label
        data.y_label = dto.y_label
        data.title = dto.title
        quantities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for test_id in acc.get_all_test_ids():
            p_values_dto = acc.get_dto_for_test(test_id)
            self.add_p_values_to_interval(quantities, p_values_dto.get_results_p_values())
        ret = []
        for i in range(10):
            ret.append([HistogramExtractor.intervals[i], quantities[i]])
        data.json_data_string = json.dumps(ret)
        ex_data = ExtractedData()
        ex_data.add_data(None, data)
        return ex_data

    def add_p_values_to_interval(self, quantities: list, p_values: list):
        for p_value in p_values:
            pos = int(math.floor(p_value * 10))
            if pos >= 10:
                pos -= 1
            quantities[pos] += 1
