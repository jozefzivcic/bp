from os.path import exists

from charts.histogram.data_for_histogram_creator import DataForHistogramCreator
from charts.histogram.histogram_creator import HistogramCreator
from charts.p_values_chart_dto import PValuesChartDto
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.generate_charts_dto import GenerateChartsDto
from charts.p_values.data_for_p_values_creator import DataForPValuesCreator
from charts.p_values.p_values_creator import PValuesCreator
from common.test_converter import TestConverter
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool
from managers.dbtestmanager import DBTestManager
from managers.resultsmanager import ResultsManager
from p_value_processing.p_values_processor import PValuesProcessor
from p_value_processing.processing_dto import ProcessingDto


class ChartsCreator:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._loaded_items = False
        self._tests_with_dirs = None
        self._tests_dao = DBTestManager(pool)
        self._results_dao = ResultsManager(pool)
        self._p_values_accumulators = {}
        self._test_converter = TestConverter()
        self._charts_storage = ChartsStorage()
        self._p_values_creator = PValuesCreator(pool, storage)
        self._histogram_creator = HistogramCreator()
        self.supported_charts = [ChartType.P_VALUES, ChartType.HISTOGRAM]

    def generate_charts(self, generate_charts_dto: GenerateChartsDto) -> ChartsStorage:
        self.check_input(generate_charts_dto)
        self.load_p_values(generate_charts_dto.test_ids)
        for chart_type, chart_dto in generate_charts_dto.chart_types.items():
            self.draw_concrete_charts(chart_type, chart_dto, generate_charts_dto.directory)
        return self._charts_storage

    def create_p_values_charts_for_tests(self, dto: PValuesChartDto, directory: str):
        for file_id, acc in self._p_values_accumulators.items():
            data_for_creator = DataForPValuesCreator(dto, acc, directory, file_id)
            chart_info = self._p_values_creator.create_p_values_chart(data_for_creator)
            self._charts_storage.add_chart_info(chart_info)

    def create_histograms_for_tests(self, dto, directory):
        for file_id, acc in self._p_values_accumulators.items():
            data_for_creator = DataForHistogramCreator(dto, acc, directory, file_id)
            chart_info = self._histogram_creator.create_histogram(data_for_creator)
            self._charts_storage.add_chart_info(chart_info)

    def load_p_values(self, test_ids):
        if self._loaded_items:
            return
        self._tests_with_dirs = self._results_dao.get_paths_for_test_ids(test_ids)
        tests = self._tests_dao.get_tests_by_id_list(test_ids)
        divided_on_files = self._test_converter.get_test_ids_for_files(tests)
        for key, value in divided_on_files.items():
            subset = self.get_subset_from_tests(value)
            processing_dto = ProcessingDto(subset)
            p_values_processor = PValuesProcessor()
            p_values_accumulator = p_values_processor.process_p_values(processing_dto)
            self._p_values_accumulators[key] = p_values_accumulator
        self._loaded_items = True

    def reset(self):
        self._loaded_items = False
        self._tests_with_dirs = None
        self._p_values_accumulators = {}
        self._charts_storage = ChartsStorage()

    def get_subset_from_tests(self, test_ids: list) -> list:
        return list(filter(lambda x: x[0] in test_ids, self._tests_with_dirs))

    def check_input(self, generate_charts_dto: GenerateChartsDto):
        if generate_charts_dto is None:
            raise TypeError('Charts DTO is None')
        if generate_charts_dto.test_ids is None:
            raise TypeError('Test ids are None')
        if not generate_charts_dto.test_ids:  # list is empty
            raise ValueError('No test ids specified')
        if generate_charts_dto.chart_types is None:
            raise TypeError('Chart types are None')
        if not generate_charts_dto.chart_types:
            raise ValueError('No chart type specified')
        if generate_charts_dto.directory is None:
            raise TypeError('Directory is None')
        if not exists(generate_charts_dto.directory):
            raise ValueError('Given directory: ' + generate_charts_dto.directory + ' does not exists')

    def draw_concrete_charts(self, chart_type: ChartType, dto, directory: str):
        if chart_type == ChartType.P_VALUES:
            self.create_p_values_charts_for_tests(dto, directory)
        elif chart_type == ChartType.HISTOGRAM:
            self.create_histograms_for_tests(dto, directory)
