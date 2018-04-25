from os.path import exists

from charts.boxplot_per_test.boxplot_pt_creator import BoxplotPTCreator
from charts.boxplot_per_test.data_for_boxplot_pt_creator import DataForBoxplotPTCreator
from charts.charts_error import ChartsError
from charts.dto.boxplot_pt_dto import BoxplotPTDto
from charts.dto.proportions_dto import ProportionsDto
from charts.ecdf.data_for_ecdf_creator import DataForEcdfCreator
from charts.ecdf.ecdf_creator import EcdfCreator
from charts.dto.ecdf_dto import EcdfDto
from charts.histogram.data_for_histogram_creator import DataForHistogramCreator
from charts.histogram.histogram_creator import HistogramCreator
from charts.dto.histogram_dto import HistogramDto
from charts.dto.p_values_chart_dto import PValuesChartDto
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.generate_charts_dto import GenerateChartsDto
from charts.p_values.data_for_p_values_creator import DataForPValuesCreator
from charts.p_values.p_values_creator import PValuesCreator
from charts.proportions.data_for_proportions_creator import DatForProportionsCreator
from charts.proportions.proportions_creator import ProportionsCreator
from charts.test_dependency.data_for_test_dependency_creator import DataForTestDependencyCreator
from charts.test_dependency.test_dependency_creator import TestDependencyCreator
from charts.dto.test_dependency_dto import TestDependencyDto
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
        self._test_dependency_creator = TestDependencyCreator(pool, storage)
        self._ecdf_creator = EcdfCreator()
        self._boxplot_pt_creator = BoxplotPTCreator(pool, storage)
        self._prop_creator = ProportionsCreator(pool, storage)
        self.supported_charts = [ChartType.P_VALUES, ChartType.P_VALUES_ZOOMED, ChartType.HISTOGRAM,
                                 ChartType.TESTS_DEPENDENCY, ChartType.ECDF, ChartType.BOXPLOT_PT,
                                 ChartType.PROPORTIONS]

    def generate_charts(self, generate_charts_dto: GenerateChartsDto) -> ChartsStorage:
        if generate_charts_dto is None:
            return None
        self.check_input(generate_charts_dto)
        self.load_p_values(generate_charts_dto.test_ids)
        for chart_type, chart_dto_list in generate_charts_dto.chart_types.items():
            for chart_dto in chart_dto_list:
                self.draw_concrete_charts(chart_type, chart_dto, generate_charts_dto.directory)
        return self._charts_storage

    def create_p_values_charts_for_tests(self, dto: PValuesChartDto, directory: str):
        for file_id, acc in self._p_values_accumulators.items():
            data_for_creator = DataForPValuesCreator(dto, acc, directory, file_id)
            chart_info = self._p_values_creator.create_p_values_chart(data_for_creator)
            self._charts_storage.add_chart_info(chart_info)

    def create_histograms_for_tests(self, dto: HistogramDto, directory: str):
        for file_id, acc in self._p_values_accumulators.items():
            data_for_creator = DataForHistogramCreator(dto, acc, directory, file_id)
            ch_storage = self._histogram_creator.create_histogram(data_for_creator)
            self._charts_storage.extend(ch_storage)

    def create_tests_dependency_charts(self, dto: TestDependencyDto, directory: str):
        for file_id, acc in self._p_values_accumulators.items():
            data_for_creator = DataForTestDependencyCreator(dto, acc, directory, file_id)
            charts_storage = self._test_dependency_creator.create_test_dependency_charts(data_for_creator)
            self._charts_storage.extend(charts_storage)

    def create_ecdf_charts(self, dto: EcdfDto, directory: str):
        for file_id, acc in self._p_values_accumulators.items():
            data_for_creator = DataForEcdfCreator(dto, acc, directory, file_id)
            charts_storage = self._ecdf_creator.create_ecdf_charts(data_for_creator)
            self._charts_storage.extend(charts_storage)

    def create_boxplots_pt(self, dto: BoxplotPTDto, directory: str):
        for file_id, acc in self._p_values_accumulators.items():
            data_for_creator = DataForBoxplotPTCreator(dto, acc, directory, file_id)
            storage = self._boxplot_pt_creator.create_boxplots(data_for_creator)
            self._charts_storage.extend(storage)

    def create_proportions(self, dto: ProportionsDto, directory: str):
        for file_id, acc in self._p_values_accumulators.items():
            data_for_creator = DatForProportionsCreator(dto, acc, directory, file_id)
            storage = self._prop_creator.create_prop_chart(data_for_creator)
            self._charts_storage.extend(storage)

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
        elif chart_type == ChartType.P_VALUES_ZOOMED:
            self.create_p_values_charts_for_tests(dto, directory)
        elif chart_type == ChartType.HISTOGRAM:
            self.create_histograms_for_tests(dto, directory)
        elif chart_type == ChartType.TESTS_DEPENDENCY:
            self.create_tests_dependency_charts(dto, directory)
        elif chart_type == ChartType.ECDF:
            self.create_ecdf_charts(dto, directory)
        elif chart_type == ChartType.BOXPLOT_PT:
            self.create_boxplots_pt(dto, directory)
        elif chart_type == ChartType.PROPORTIONS:
            self.create_proportions(dto, directory)
        else:
            raise ChartsError('Unsupported chart type')
