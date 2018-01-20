from os.path import dirname, abspath, join
from tempfile import mkdtemp

from shutil import rmtree

from charts.chart_options import ChartOptions
from charts.chart_type import ChartType
from charts.charts_creator import ChartsCreator
from charts.charts_error import ChartsError
from charts.charts_storage import ChartsStorage
from charts.generate_charts_dto import GenerateChartsDto
from common.helper_functions import load_texts_for_generator
from configstorage import ConfigStorage
from managers.connectionpool import ConnectionPool
from pdf_generating.pdf_creating_dto import PdfCreatingDto
from pdf_generating.pdf_creating_error import PdfCreatingError
from pdf_generating.pdf_creator import PdfCreator
from pdf_generating.pdf_generating_dto import PdfGeneratingDto
from pdf_generating.pdf_generating_error import PdfGeneratingError

this_dir = dirname(abspath(__file__))


class PdfGenerator:
    def __init__(self, pool: ConnectionPool, storage: ConfigStorage):
        self._charts_creator = ChartsCreator(pool, storage)
        self._pdf_creator = PdfCreator()
        path_to_texts = abspath(join(this_dir, storage.path_to_pdf_texts))
        self._texts = load_texts_for_generator(path_to_texts)
        self._texts['vars'] = {}
        self.path_to_templates = abspath(join(this_dir, storage.path_to_tex_templates))

    def generate_pdf(self, pdf_generating_dto: PdfGeneratingDto):
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
            dto = ChartOptions(pdf_generating_dto.alpha, texts['general']['tests'],
                               texts['general']['pvalue'], texts['pvalueschart']['pvalueschart'])
            return dto
        raise PdfGeneratingError('Unsupported chart type')

    def prepare_pdf_creating_dto(self, pdf_generating_dto: PdfGeneratingDto, storage: ChartsStorage) -> PdfCreatingDto:
        dto = PdfCreatingDto()
        return dto
