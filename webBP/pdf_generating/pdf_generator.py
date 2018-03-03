from os.path import dirname, abspath, join
from shutil import rmtree
from tempfile import mkdtemp

from charts.chart_info import ChartInfo
from charts.dto.ecdf_dto import EcdfDto
from charts.dto.histogram_dto import HistogramDto
from charts.dto.p_values_chart_dto import PValuesChartDto
from charts.chart_type import ChartType
from charts.charts_creator import ChartsCreator
from charts.charts_error import ChartsError
from charts.charts_storage import ChartsStorage
from charts.generate_charts_dto import GenerateChartsDto
from charts.dto.test_dependency_dto import TestDependencyDto
from common.helper_functions import load_texts_into_config_parsers, escape_latex_special_chars, \
    convert_specs_to_seq_acc, convert_specs_to_p_value_seq
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool
from managers.dbtestmanager import DBTestManager
from managers.filemanager import FileManager
from managers.nisttestmanager import NistTestManager
from p_value_processing.p_values_file_type import PValuesFileType
from pdf_generating.pdf_creating_dto import PdfCreatingDto
from pdf_generating.pdf_creating_error import PdfCreatingError
from pdf_generating.pdf_creator import PdfCreator
from pdf_generating.pdf_generating_dto import PdfGeneratingDto
from pdf_generating.pdf_generating_error import PdfGeneratingError

this_dir = dirname(abspath(__file__))


class PdfGenerator:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self.config_storage = storage
        self._test_dao = DBTestManager(pool)
        self._nist_dao = NistTestManager(pool)
        self._file_dao = FileManager(pool)
        self._charts_creator = ChartsCreator(pool, storage)
        self._pdf_creator = PdfCreator()
        path_to_texts = abspath(join(this_dir, storage.path_to_pdf_texts))
        self._texts = load_texts_into_config_parsers(path_to_texts)
        self.supported_languages = {'en': 'english'}

    def generate_pdf(self, pdf_generating_dto: PdfGeneratingDto):
        self.check_input(pdf_generating_dto)
        directory = mkdtemp()
        try:
            generate_dto = self.prepare_generate_charts_dto(pdf_generating_dto, directory)
            storage = self._charts_creator.generate_charts(generate_dto)
            pdf_creating_dto = self.prepare_pdf_creating_dto(pdf_generating_dto, storage)
            self._pdf_creator.create_pdf(pdf_creating_dto)
        except (ChartsError, PdfCreatingError) as e:
            raise PdfGeneratingError(e)
        finally:
            rmtree(directory)

    def prepare_generate_charts_dto(self, pdf_generating_dto: PdfGeneratingDto, directory: str) -> GenerateChartsDto:
        dict_for_dto = {}
        for chart_type in pdf_generating_dto.chart_types:
            dict_for_dto[chart_type] = self.create_dto_for_concrete_chart(chart_type, pdf_generating_dto)
        charts_dto = GenerateChartsDto(pdf_generating_dto.test_ids, dict_for_dto, directory)
        return charts_dto

    def create_dto_for_concrete_chart(self, chart_type: ChartType, pdf_generating_dto: PdfGeneratingDto):
        texts = self._texts[pdf_generating_dto.language]
        if chart_type == ChartType.P_VALUES:
            dto = PValuesChartDto(pdf_generating_dto.alpha, texts['General']['Tests'],
                                  texts['General']['PValue'], texts['PValuesChart']['PValuesChart'])
            return [dto]
        elif chart_type == ChartType.P_VALUES_ZOOMED:
            dto = PValuesChartDto(pdf_generating_dto.alpha, texts['General']['Tests'],
                                  texts['General']['PValue'], texts['PValuesChart']['PValuesChart'], True)
            return [dto]
        elif chart_type == ChartType.HISTOGRAM:
            dto = HistogramDto(texts['Histogram']['Intervals'], texts['Histogram']['NumOfPValues'],
                               texts['Histogram']['Histogram'])
            return [dto]
        elif chart_type == ChartType.TESTS_DEPENDENCY:
            try:
                specs = pdf_generating_dto.test_dependency_options.test_file_specs
                seq_acc = convert_specs_to_seq_acc(specs)
            except ValueError as e:
                raise PdfGeneratingError(e)
            dto = TestDependencyDto(seq_acc, texts['TestDependency']['Title'])
            return [dto]
        elif chart_type == ChartType.ECDF:
            try:
                specs = pdf_generating_dto.ecdf_options.test_file_specs
                p_value_seqcs = convert_specs_to_p_value_seq(specs)
            except (ValueError, TypeError, RuntimeError) as e:
                raise PdfGeneratingError(e)
            dto = EcdfDto(pdf_generating_dto.alpha, texts['ECDF']['Title'], texts['ECDF']['XLabel'],
                          texts['ECDF']['YLabel'], texts['ECDF']['EmpiricalLabel'], texts['ECDF']['TheoreticalLabel'],
                          p_value_seqcs)
            return [dto]
        raise PdfGeneratingError('Unsupported chart type')

    def prepare_pdf_creating_dto(self, pdf_generating_dto: PdfGeneratingDto, storage: ChartsStorage) -> PdfCreatingDto:
        template_path = abspath(join(this_dir, self.config_storage.path_to_tex_templates, 'report_template.tex'))
        vars_dict = self.prepare_dict_from_charts_storage(storage, pdf_generating_dto.language)
        config_parser = self._texts[pdf_generating_dto.language]
        keys_for_template = {'texts': config_parser, 'vars': {'package_language':
                                                                  self.supported_languages[pdf_generating_dto.language],
                                                              'charts': vars_dict}}
        dto = PdfCreatingDto(template_path, pdf_generating_dto.output_filename, keys_for_template)
        return dto

    def prepare_dict_from_charts_storage(self, storage: ChartsStorage, language: str) -> dict:
        charts_dict = {}
        for chart_info in storage.get_all_infos():
            fid = chart_info.file_id
            file_name = self.get_file_name(fid)
            file_name = escape_latex_special_chars(file_name)
            chart_name = self.get_chart_name(language, chart_info)
            if fid in charts_dict:
                charts_dict[fid]['chart_info'].append({'path_to_chart': chart_info.path_to_chart,
                                                       'chart_type': chart_info.chart_type.name,
                                                       'chart_name': chart_name
                                                       })
            else:
                charts_dict[fid] = {'file_name': file_name,
                                    'chart_info': [{'path_to_chart': chart_info.path_to_chart,
                                                    'chart_type': chart_info.chart_type.name,
                                                    'chart_name': chart_name
                                                    }]
                                    }
        return charts_dict

    def get_file_name(self, fid: int):
        return self._file_dao.get_file_by_id(fid).name

    def check_input(self, dto: PdfGeneratingDto):
        if dto.language not in self.supported_languages.keys():
            raise PdfGeneratingError('Unsupported language (\'' + dto.language + '\')')
        for ch_type in dto.chart_types:
            if ch_type not in self._charts_creator.supported_charts:
                raise PdfGeneratingError('Unsupported chart type: (\'' + str(ch_type) + '\')')
        if ChartType.TESTS_DEPENDENCY in dto.chart_types:
            if dto.test_dependency_options is None:
                raise PdfGeneratingError('No default options for test dependency chart')
            if not dto.test_dependency_options:
                raise PdfGeneratingError('No pair of tests for test dependency chart')
        if ChartType.ECDF in dto.chart_types:
            if dto.ecdf_options is None:
                raise PdfGeneratingError('No default options for ecdf chart')
            if not dto.ecdf_options:
                raise PdfGeneratingError('No test for ECDF chart')

    def get_chart_name(self, language: str, info: ChartInfo) -> str:
        ch_type = info.chart_type
        if ch_type == ChartType.P_VALUES:
            return self._texts[language]['PValuesChart']['PValuesChart']
        elif ch_type == ChartType.P_VALUES_ZOOMED:
            return self._texts[language]['PValuesChartZoomed']['PValuesChartZoomed']
        elif ch_type == ChartType.HISTOGRAM:
            return self._texts[language]['Histogram']['HistogramUpperH']
        elif ch_type == ChartType.TESTS_DEPENDENCY:
            return self._texts[language]['TestDependency']['Title']
        elif ch_type == ChartType.ECDF:
            return self.get_ecdf_chart_name(language, info)
        raise PdfGeneratingError('Undefined chart type: ' + str(ch_type))

    def get_ecdf_chart_name(self, language: str, info: ChartInfo):
        title = '{} {}'.format(self._texts[language]['ECDF']['Title'], self._texts[language]['General']['From'])
        seq = info.ds_info.p_value_sequence
        test_id = seq.test_id
        test = self._test_dao.get_test_by_id(test_id)
        test_name = self._nist_dao.get_nist_param_for_test(test).get_test_name()
        title += ' {}'.format(test_name)
        if seq.p_values_file == PValuesFileType.RESULTS:
            return title + ' {}'.format(self._texts[language]['General']['Results'])
        elif seq.p_values_file == PValuesFileType.DATA:
            return title + ' {} {}'.format(self._texts[language]['General']['Data'], seq.data_num)
        else:
            raise RuntimeError('Unknown file type {}'.format(seq.p_values_file))
