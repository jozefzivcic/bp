import json
from unittest import TestCase

from charts.histogram.historam_extractor import HistogramExtractor
from charts.dto.histogram_dto import HistogramDto
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14

intervals = ['[0.0, 0.1)', '[0.1, 0.2)', '[0.2, 0.3)', '[0.3, 0.4)', '[0.4, 0.5)', '[0.5, 0.6)', '[0.6, 0.7)',
             '[0.7, 0.8)', '[0.8, 0.9)', '[0.9, 1.0]']


class TestHistogramExtractor(TestCase):
    def setUp(self):
        self.extractor = HistogramExtractor()
        self.quantities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sample_p_values = [0.779952, 0.468925, 0.468925, 0.511232, 0.462545, 0.666913, 0.171598, 0.375557,
                                0.746548, 0.558648]
        self.expected_quantities = [0, 1, 0, 1, 3, 2, 1, 2, 0, 0]

    def test_add_p_values_to_interval_random_p_values(self):
        self.extractor.add_p_values_to_interval(self.quantities, self.sample_p_values)
        self.assertEqual(self.expected_quantities, self.quantities)

    def test_add_p_values_to_interval_mid_interval(self):
        p_values = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
        expected_quantities = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.extractor.add_p_values_to_interval(self.quantities, p_values)
        self.assertEqual(expected_quantities, self.quantities)

    def test_add_p_values_to_interval_boundary(self):
        p_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        expected_quantities = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        self.extractor.add_p_values_to_interval(self.quantities, p_values)
        self.assertEqual(expected_quantities, self.quantities)

        expected_quantities = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        self.extractor.add_p_values_to_interval(self.quantities, p_values)
        self.assertEqual(expected_quantities, self.quantities)

    def test_get_data_from_accumulator_none_ds_info(self):
        test1_id = 456
        test2_id = 457
        dto1 = PValuesDto(dict_for_test_13)
        dto2 = PValuesDto(dict_for_test_14)
        acc = PValuesAccumulator()
        acc.add(test1_id, dto1)
        acc.add(test2_id, dto2)
        hist_dto = HistogramDto('x_label', 'y_label', 'title')
        ret = self.extractor.get_data_from_accumulator(acc, hist_dto)
        ds_info = ret.get_all_data()[0][0]
        self.assertIsNone(ds_info)

    def test_get_data_from_accumulator(self):
        dto1 = PValuesDto({'results': self.sample_p_values})

        p_values_2 = [x + 0.1 for x in self.sample_p_values]
        data1 = []
        data2 = []
        for i in range(10):
            if i % 2 == 0:
                data1.append(p_values_2[i])
            else:
                data2.append(p_values_2[i])
        expected_quantities_2 = [0, 0, 1, 0, 1, 3, 2, 1, 2, 0]
        dto2 = PValuesDto({'results': p_values_2, 'data1': data1, 'data2': data2})

        test1_id = 456
        test2_id = 457
        acc = PValuesAccumulator()
        acc.add(test1_id, dto1)
        acc.add(test2_id, dto2)

        hist_dto = HistogramDto('x_label', 'y_label', 'title')

        total_quantities = [x + y for x, y in zip(self.expected_quantities, expected_quantities_2)]
        data = []
        for i in range(10):
            data.append([intervals[i], total_quantities[i]])
        json_data = json.dumps(data)

        extracted_data = self.extractor.get_data_from_accumulator(acc, hist_dto)
        ret = extracted_data.get_all_data()[0][1]

        self.assertEqual(hist_dto.x_label, ret.x_label)
        self.assertEqual(hist_dto.y_label, ret.y_label)
        self.assertEqual(hist_dto.title, ret.title)
        self.assertEqual(json_data, ret.json_data_string)
