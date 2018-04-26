from configparser import ConfigParser
from os.path import dirname, abspath, join
from shutil import rmtree
from tempfile import mkdtemp

from charts.chart_info import ChartInfo
from charts.dto.boxplot_pt_dto import BoxplotPTDto
from charts.dto.ecdf_dto import EcdfDto
from charts.dto.histogram_dto import HistogramDto
from charts.dto.p_values_chart_dto import PValuesChartDto
from charts.chart_type import ChartType
from charts.charts_creator import ChartsCreator
from charts.charts_error import ChartsError
from charts.charts_storage import ChartsStorage
from charts.dto.proportions_dto import ProportionsDto
from charts.generate_charts_dto import GenerateChartsDto
from charts.dto.test_dependency_dto import TestDependencyDto
from charts.tests_in_chart import TestsInChart
from common.error.err import Err
from common.helper_functions import load_texts_into_config_parsers, escape_latex_special_chars, \
    convert_specs_to_seq_acc, convert_specs_to_p_value_seq, specs_list_to_p_value_seq_list
from common.info.info import Info
from configstorage import ConfigStorage
from enums.nist_test_type import NistTestType
from managers.connectionpool import ConnectionPool
from managers.dbtestmanager import DBTestManager
from managers.filemanager import FileManager
from managers.nisttestmanager import NistTestManager
from nist_statistics.statistics_creator import StatisticsCreator
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.p_values_processing_error import PValuesProcessingError
from pdf_generating.pdf_creating_dto import PdfCreatingDto
from pdf_generating.pdf_creating_error import PdfCreatingError
from pdf_generating.pdf_creator import PdfCreator
from pdf_generating.pdf_generating_dto import PdfGeneratingDto
from pdf_generating.pdf_generating_error import PdfGeneratingError
from pdf_generating.report_to_latex import convert_report_to_latex

this_dir = dirname(abspath(__file__))


class PdfGenerator:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self.config_storage = storage
        self._test_dao = DBTestManager(pool)
        self._nist_dao = NistTestManager(pool)
        self._file_dao = FileManager(pool)
        self._charts_creator = ChartsCreator(pool, storage)
        self._stats_creator = StatisticsCreator(pool, storage)
        self._pdf_creator = PdfCreator()
        path_to_texts = abspath(join(this_dir, storage.path_to_pdf_texts))
        self._texts = load_texts_into_config_parsers(path_to_texts)
        self._short_test_names_dict = self.get_short_tests_names(self._texts)
        self.supported_languages = {'en': 'english'}

    def generate_pdf(self, pdf_generating_dto: PdfGeneratingDto):
        self.check_input(pdf_generating_dto)
        directory = mkdtemp()
        try:
            generate_dto = self.prepare_generate_charts_dto(pdf_generating_dto, directory)
            storage = self._charts_creator.generate_charts(generate_dto)
            stats_dict = self.create_nist_report(pdf_generating_dto, directory)
            pdf_creating_dto = self.prepare_pdf_creating_dto(pdf_generating_dto, storage, stats_dict)
            self._pdf_creator.create_pdf(pdf_creating_dto)
        except (ChartsError, PdfCreatingError, PValuesProcessingError) as e:
            raise PdfGeneratingError(e)
        finally:
            rmtree(directory)

    def prepare_generate_charts_dto(self, pdf_generating_dto: PdfGeneratingDto, directory: str) -> GenerateChartsDto:
        if not pdf_generating_dto.chart_types:
            return None
        dict_for_dto = {}
        for chart_type in pdf_generating_dto.chart_types:
            dict_for_dto[chart_type] = self.create_dto_for_concrete_chart(chart_type, pdf_generating_dto)
        charts_dto = GenerateChartsDto(pdf_generating_dto.test_ids, dict_for_dto, directory)
        return charts_dto

    def create_dto_for_concrete_chart(self, chart_type: ChartType, pdf_generating_dto: PdfGeneratingDto):
        texts = self._texts[pdf_generating_dto.language]
        if chart_type == ChartType.P_VALUES:
            dto = PValuesChartDto(pdf_generating_dto.alpha, texts['General']['Tests'],
                                  texts['General']['PValue'], texts['PValuesChart']['PValuesChart'], False,
                                  self._short_test_names_dict[pdf_generating_dto.language])
            return [dto]
        elif chart_type == ChartType.P_VALUES_ZOOMED:
            dto = PValuesChartDto(pdf_generating_dto.alpha, texts['General']['Tests'],
                                  texts['General']['PValue'], texts['PValuesChart']['PValuesChart'], True,
                                  self._short_test_names_dict[pdf_generating_dto.language])
            return [dto]
        elif chart_type == ChartType.HISTOGRAM:
            options = pdf_generating_dto.hist_options
            dto = HistogramDto(texts['Histogram']['Intervals'], texts['Histogram']['NumOfPValues'],
                               texts['Histogram']['Histogram'], options.hist_for_tests)
            return [dto]
        elif chart_type == ChartType.TESTS_DEPENDENCY:
            try:
                specs = pdf_generating_dto.test_dependency_options.test_file_specs
                seq_acc = convert_specs_to_seq_acc(specs)
            except ValueError as e:
                raise PdfGeneratingError(e)
            filter_unif = pdf_generating_dto.test_dependency_options.filter_unif
            dto = TestDependencyDto(pdf_generating_dto.alpha, filter_unif, seq_acc, texts['TestDependency']['Title'],
                                    pdf_generating_dto.test_dependency_options.test_pairs,
                                    self._short_test_names_dict[pdf_generating_dto.language])
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
        elif chart_type == ChartType.BOXPLOT_PT:
            try:
                specs = pdf_generating_dto.boxplot_pt_options.test_file_specs
                converted = specs_list_to_p_value_seq_list(specs)
            except (ValueError, TypeError, RuntimeError) as e:
                raise PdfGeneratingError(e)
            dto = BoxplotPTDto(texts['BoxplotPT']['Title'], converted,
                               self._short_test_names_dict[pdf_generating_dto.language])
            return [dto]
        elif chart_type == ChartType.PROPORTIONS:
            dto = ProportionsDto(pdf_generating_dto.alpha, texts['Proportions']['Title'], texts['General']['Tests'],
                                 texts['Proportions']['Proportion'], pdf_generating_dto.prop_options.formula,
                                 self._short_test_names_dict[pdf_generating_dto.language])
            return [dto]
        raise PdfGeneratingError('Unsupported chart type')

    def prepare_pdf_creating_dto(self, pdf_generating_dto: PdfGeneratingDto, storage: ChartsStorage, stats_dict: dict) \
            -> PdfCreatingDto:
        template_path = abspath(join(this_dir, self.config_storage.path_to_tex_templates, 'report_template.tex'))
        vars_dict = self.prepare_dict_from_charts_storage(storage, pdf_generating_dto.language)
        config_parser = self._texts[pdf_generating_dto.language]
        nist_dict = self.prepare_nist_report_dict(stats_dict, pdf_generating_dto.language)
        keys_for_template = {'texts': config_parser, 'vars': {'package_language':
                                                                  self.supported_languages[pdf_generating_dto.language],
                                                              'charts': vars_dict,
                                                              'nist_report_dict': nist_dict}}
        dto = PdfCreatingDto(template_path, pdf_generating_dto.output_filename, keys_for_template)
        return dto

    def prepare_dict_from_charts_storage(self, storage: ChartsStorage, language: str) -> dict:
        if storage is None:
            return None
        files_dict = {}
        for cs_item in storage.get_all_items():
            chart_info = cs_item.ch_info
            fid = chart_info.file_id
            file_name = self.get_file_name(fid)
            file_name = escape_latex_special_chars(file_name)
            my_dict = self.get_chart_dict(language, chart_info, cs_item.info, cs_item.err)
            if fid in files_dict:
                files_dict[fid]['chart_info'].append(my_dict)
            else:
                files_dict[fid] = {'file_name': file_name, 'chart_info': [my_dict]}
        self.sort_files_dict(files_dict)
        charts_dict = {'files': files_dict}
        self.add_infos(language, charts_dict, storage)
        self.add_errors(language, charts_dict, storage)
        return charts_dict

    def get_chart_dict(self, language: str, ch_info: ChartInfo, info: Info = None, err: Err = None):
        chart_name = self.get_chart_name(language, ch_info)
        my_dict = {'path_to_chart': ch_info.path_to_chart,
                   'chart_type': ch_info.chart_type,
                   'chart_name': chart_name
                   }
        if info is not None:
            info_msg = info.get_message(self._texts[language])
            info_msg = escape_latex_special_chars(info_msg)
            my_dict['info_msg'] = info_msg
        if err is not None:
            err_msg = err.get_message(self._texts[language])
            err_msg = escape_latex_special_chars(err_msg)
            my_dict['err_msg'] = err_msg
        return my_dict

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
        if ChartType.BOXPLOT_PT in dto.chart_types:
            if dto.boxplot_pt_options is None:
                raise PdfGeneratingError('No default options for Boxplot')
            if not dto.boxplot_pt_options:
                raise PdfGeneratingError('No tests for boxplot selected')
        if ChartType.PROPORTIONS in dto.chart_types:
            if dto.prop_options is None:
                raise PdfGeneratingError('No default options for proportions')

    def get_chart_name_base(self, language, ch_type: ChartType) -> str:
        if ch_type == ChartType.P_VALUES:
            return self._texts[language]['PValuesChart']['PValuesChart']
        elif ch_type == ChartType.P_VALUES_ZOOMED:
            return self._texts[language]['PValuesChartZoomed']['PValuesChartZoomed']
        elif ch_type == ChartType.HISTOGRAM:
            return self._texts[language]['Histogram']['HistogramUpperH']
        elif ch_type == ChartType.TESTS_DEPENDENCY:
            return self._texts[language]['TestDependency']['Title']
        elif ch_type == ChartType.ECDF:
            return self._texts[language]['ECDF']['Title']
        elif ch_type == ChartType.BOXPLOT_PT:
            return self._texts[language]['BoxplotPT']['Title']
        elif ch_type == ChartType.PROPORTIONS:
            return self._texts[language]['Proportions']['Title']
        raise PdfGeneratingError('Undefined chart type: ' + str(ch_type))

    def get_chart_name(self, language: str, info: ChartInfo) -> str:
        ch_type = info.chart_type
        if ch_type == ChartType.ECDF:
            return self.get_ecdf_chart_name(language, info)
        elif ch_type == ChartType.HISTOGRAM:
            return self.get_hist_name(language, info)
        else:
            return self.get_chart_name_base(language, ch_type)

    def get_ecdf_chart_name(self, language: str, info: ChartInfo):
        title = '{} {}'.format(self._texts[language]['ECDF']['Title'], self._texts[language]['General']['From'])
        seq = info.ds_info.p_value_sequence
        test_id = seq.test_id
        test = self._test_dao.get_test_by_id(test_id)
        nist_param = self._nist_dao.get_nist_param_for_test(test)
        test_type = nist_param.get_test_type()
        test_name = self._short_test_names_dict[language].get(test_type)
        title += ' {}'.format(test_name)
        if seq.p_values_file == PValuesFileType.RESULTS:
            title += ' {}'.format(self._texts[language]['General']['Results'])
        elif seq.p_values_file == PValuesFileType.DATA:
            title += ' {} {}'.format(self._texts[language]['General']['Data'], seq.data_num)
        else:
            raise RuntimeError('Unknown file type {}'.format(seq.p_values_file))
        if nist_param.has_special_parameter():
            title += ' ({})'.format(nist_param.special_parameter)
        return title

    def get_hist_name(self, language: str, info: ChartInfo):
        t_in_chart = info.ds_info.tests_in_chart
        if t_in_chart == TestsInChart.MULTIPLE_TESTS:
            return self._texts[language]['Histogram']['HistAll']
        hist = self._texts[language]['Histogram']['HistogramUpperH']
        seq = info.ds_info.p_value_sequence  # type: PValueSequence
        test = self._test_dao.get_test_by_id(seq.test_id)
        param = self._nist_dao.get_nist_param_for_test(test)
        t_type = param.get_test_type()
        test_name = self._short_test_names_dict['en'].get(t_type)
        ret = '{} {}'.format(hist, test_name)
        if seq.p_values_file == PValuesFileType.DATA:
            ret += ' data {}'.format(seq.data_num)
        if param.has_special_parameter():
            ret += ' ({})'.format(param.special_parameter)
        return ret

    def add_infos(self, language: str, charts_dict: dict, storage: ChartsStorage):
        infos_dict = {}
        for ch_type in ChartType:
            infos = storage.get_infos_for_chart_type_safe(ch_type)
            if infos is None:
                continue
            messages = []
            for info in infos:
                m = info.get_message(self._texts[language])
                messages.append(m)
            if messages:
                base_name = self.get_chart_name_base(language, ch_type)
                escaped = escape_latex_special_chars(base_name)
                infos_dict[escaped] = messages
        if infos_dict:
            charts_dict['infos'] = infos_dict

    def add_errors(self, language: str, charts_dict: dict, storage: ChartsStorage):
        errors_dict = {}
        for ch_type in ChartType:
            errors = storage.get_errors_for_chart_type_safe(ch_type)
            if errors is None:
                continue
            messages = []
            for err in errors:
                m = err.get_message(self._texts[language])
                messages.append(m)
            if messages:
                base_name = self.get_chart_name_base(language, ch_type)
                escaped = escape_latex_special_chars(base_name)
                errors_dict[escaped] = messages
        if errors_dict:
            charts_dict['errors'] = errors_dict

    def create_nist_report(self, dto: PdfGeneratingDto, directory: str) -> dict:
        if not dto.create_nist_report:
            return None
        return self._stats_creator.create_stats_for_tests_ids(dto.test_ids, directory, dto.alpha)

    def prepare_nist_report_dict(self, stats_dict: dict, language: str):
        if stats_dict is None:
            return None
        ret = {}
        for key, value in stats_dict.items():
            content = convert_report_to_latex(value, self._texts[language])
            file_name = self._file_dao.get_file_by_id(key).name
            file_name = escape_latex_special_chars(file_name)
            report_data = {'content': content, 'file_name': file_name}
            ret[key] = report_data
        return ret

    def get_short_tests_names(self, texts: dict):
        ret = {}
        for key, cfg in texts.items():  # type: (str, ConfigParser)
            temp_dict = {}
            temp_dict[NistTestType.TEST_FREQUENCY] = cfg.get('ShortNames', 'Freq')
            temp_dict[NistTestType.TEST_BLOCK_FREQUENCY] = cfg.get('ShortNames', 'BFreq')
            temp_dict[NistTestType.TEST_CUSUM] = cfg.get('ShortNames', 'CuSums')
            temp_dict[NistTestType.TEST_RUNS] = cfg.get('ShortNames', 'Runs')
            temp_dict[NistTestType.TEST_LONGEST_RUN] = cfg.get('ShortNames', 'LongRun')
            temp_dict[NistTestType.TEST_RANK] = cfg.get('ShortNames', 'Rank')
            temp_dict[NistTestType.TEST_FFT] = cfg.get('ShortNames', 'FFT')
            temp_dict[NistTestType.TEST_NONPERIODIC] = cfg.get('ShortNames', 'Nonperiodic')
            temp_dict[NistTestType.TEST_OVERLAPPING] = cfg.get('ShortNames', 'Overlapping')
            temp_dict[NistTestType.TEST_UNIVERSAL] = cfg.get('ShortNames', 'Universal')
            temp_dict[NistTestType.TEST_APEN] = cfg.get('ShortNames', 'Approx')
            temp_dict[NistTestType.TEST_RND_EXCURSION] = cfg.get('ShortNames', 'RandExcs')
            temp_dict[NistTestType.TEST_RND_EXCURSION_VAR] = cfg.get('ShortNames', 'RandExcsVar')
            temp_dict[NistTestType.TEST_SERIAL] = cfg.get('ShortNames', 'Serial')
            temp_dict[NistTestType.TEST_LINEARCOMPLEXITY] = cfg.get('ShortNames', 'Linear')
            ret[key] = temp_dict
        return ret

    def sort_files_dict(self, files_dict: dict):
        for fid, value_dict in files_dict.items():
            arr = value_dict['chart_info']
            sorted_arr = sorted(arr, key=lambda x: (x['chart_type'], x['path_to_chart']))
            value_dict['chart_info'] = sorted_arr
