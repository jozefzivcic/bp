from charts.chart_options import ChartOptions
from charts.charts_error import ChartsError
from common.test_converter import TestConverter
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool
from managers.dbtestmanager import DBTestManager
from managers.resultsmanager import ResultsManager
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_processor import PValuesProcessor
from p_value_processing.processing_dto import ProcessingDto


class ChartsCreator:
    def __init__(self, chart_options: ChartOptions, pool: ConnectionPool, storage: ConfigStorage):
        self._loaded_items = False
        self._tests_with_dirs = None
        self._tests_dao = DBTestManager(pool)
        self._results_dao = ResultsManager(pool)
        self._p_values_accumulators = {}
        self.test_converter = TestConverter()

    def create_line_charts_for_tests(self, test_ids: list):
        self.load_p_values(test_ids)

    def create_one_line_chart_for_tests(self, test_ids):
        if self._tests_with_dirs is None:
            raise ChartsError('No tests are loaded')

    def load_p_values(self, test_ids):
        if self._loaded_items:
            return
        self._tests_with_dirs = self._results_dao.get_paths_for_test_ids(test_ids)
        tests = self._tests_dao.get_tests_by_id_list(test_ids)
        divided_on_files = self.test_converter.get_test_ids_for_files(tests)
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

    def get_subset_from_tests(self, test_ids: list) -> list:
        return list(filter(lambda x: x[0] in test_ids, self._tests_with_dirs))
