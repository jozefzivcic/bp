from os.path import dirname, abspath, join
from shutil import rmtree
from tempfile import mkdtemp

from charts.p_values_chart_dto import PValuesChartDto
from charts.chart_type import ChartType
from charts.charts_creator import ChartsCreator
from charts.charts_error import ChartsError
from charts.charts_storage import ChartsStorage
from charts.generate_charts_dto import GenerateChartsDto
from common.helper_functions import load_texts_into_config_parsers
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool
from managers.filemanager import FileManager
from pdf_generating.pdf_creating_dto import PdfCreatingDto
from pdf_generating.pdf_creating_error import PdfCreatingError
from pdf_generating.pdf_creator import PdfCreator
from pdf_generating.pdf_generating_dto import PdfGeneratingDto
from pdf_generating.pdf_generating_error import PdfGeneratingError

this_dir = dirname(abspath(__file__))


class PdfGenerator:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self.config_storage = storage
        self.file_dao = FileManager(pool)
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
            return dto
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
            chart_name = self.get_chart_name(language, chart_info.chart_type)
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
        return self.file_dao.get_file_by_id(fid).name

    def check_input(self, pdf_generating_dto: PdfGeneratingDto):
        if pdf_generating_dto.language not in self.supported_languages.keys():
            raise PdfGeneratingError('Unsupported language (\'' + pdf_generating_dto.language + '\')')
        for ch_type in pdf_generating_dto.chart_types:
            if ch_type not in self._charts_creator.supported_charts:
                raise PdfGeneratingError('Unsupported chart type: (\'' + str(ch_type) + '\')')

    def get_chart_name(self, language: str, ch_type: ChartType) -> str:
        if ch_type == ChartType.P_VALUES:
            return self._texts[language]['PValuesChart']['PValuesChart']
        raise PdfGeneratingError('Undefined chart type: ' + ch_type.name)
