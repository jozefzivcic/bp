from os.path import join, exists

from charts.chart_options import ChartOptions
from charts.charts_error import ChartsError
from charts.p_values.extractor import Extractor
from charts.p_values.p_values_drawer import PValuesDrawer
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
        self._extractor = Extractor(chart_options, pool, storage)
        self.p_values_drawer = PValuesDrawer()

    def create_p_values_charts_for_tests(self, test_ids: list, directory: str):
        self.check_test_ids_and_dir(test_ids, directory)

        self.load_p_values(test_ids)
        for file_id, acc in self._p_values_accumulators.items():
            file_name = self.get_file_name_for_p_values_chart(directory, file_id)
            self.create_one_p_values_chart_for_tests(acc, file_name)

    def create_one_p_values_chart_for_tests(self, acc: PValuesAccumulator, file: str):
        if acc is None:
            raise TypeError('Accumulator cannot be None')
        if file is None:
            raise TypeError('File cannot be None')
        data_for_chart = self._extractor.get_data_from_accumulator(acc)
        self.p_values_drawer.draw_chart(data_for_chart, file)

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

    def get_file_name_for_p_values_chart(self, directory, file_id):
        file_name = 'p_values_for_file_' + str(file_id) + '.png'
        return join(directory, file_name)

    def check_test_ids_and_dir(self, test_ids, directory):
        if test_ids is None:
            raise TypeError('Test ids are None')
        if not test_ids:  # list is empty
            raise ValueError('No test ids specified')
        if directory is None:
            raise TypeError('Directory is None')
        if not exists(directory):
            raise ValueError('Given directory: ' + directory + ' does not exists')
