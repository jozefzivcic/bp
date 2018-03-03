from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from charts.chart_type import ChartType
from charts.histogram.data_for_histogram_creator import DataForHistogramCreator
from charts.histogram.histogram_creator import HistogramCreator
from charts.dto.histogram_dto import HistogramDto
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_histogram_creator')


class TestHistogramCreator(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        dto1 = PValuesDto({'results': [0.779952, 0.468925, 0.468925, 0.511232, 0.462545, 0.666913, 0.171598, 0.375557,
                                       0.746548, 0.558648]})
        dto2 = PValuesDto({'results': [0.879952, 0.568925, 0.568925, 0.611232, 0.562545, 0.766913, 0.271598, 0.475557,
                                       0.846548, 0.658648]})
        acc = PValuesAccumulator()
        acc.add(456, dto1)
        acc.add(654, dto2)

        hist_dto = HistogramDto('intervals', 'number of p-values', 'histogram')
        self.data_for_creator = DataForHistogramCreator(hist_dto, acc, working_dir, 789)
        self.creator = HistogramCreator()

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_create_p_values_chart(self):
        ch_info = self.creator.create_histogram(self.data_for_creator)
        self.assertTrue(exists(ch_info.path_to_chart))
        self.assertEqual(ChartType.HISTOGRAM, ch_info.chart_type)
        self.assertEqual(self.data_for_creator.file_id, ch_info.file_id)

    def test_get_file_name_for_chart(self):
        expected = join(working_dir, 'histogram_for_file_' + str(self.data_for_creator.file_id) + '.png')
        ret = self.creator.get_file_name_for_chart(working_dir, self.data_for_creator.file_id)
        self.assertEqual(expected, ret)

    def test_check_input_none_data(self):
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(None)
        self.assertEqual('Data is None', str(context.exception))

    def test_check_input_none_histogram_dto(self):
        self.data_for_creator.histogram_dto = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(self.data_for_creator)
        self.assertEqual('Histogram DTO is None', str(context.exception))

    def test_check_input_none_accumulator(self):
        self.data_for_creator.acc = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(self.data_for_creator)
        self.assertEqual('Accumulator is None', str(context.exception))

    def test_check_input_none_directory(self):
        self.data_for_creator.directory = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(self.data_for_creator)
        self.assertEqual('Directory is None', str(context.exception))

    def test_check_input_none_file_id(self):
        self.data_for_creator.file_id = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_histogram(self.data_for_creator)
        self.assertEqual('File id is None', str(context.exception))
