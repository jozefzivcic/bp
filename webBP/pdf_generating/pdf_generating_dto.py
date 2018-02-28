from pdf_generating.options.ecdf_options import EcdfOptions
from pdf_generating.options.test_dependency_options import TestDependencyOptions


class PdfGeneratingDto:
    def __init__(self, alpha: float=0.01, test_ids: list=None, chart_types: list=None, language: str=None,
                 output_filename: str=None, test_dependency_options: TestDependencyOptions=None,
                 ecdf_options: EcdfOptions=None):
        self.alpha = alpha
        self.test_ids = test_ids
        self.chart_types = chart_types
        self.language = language
        self.output_filename = output_filename
        self.test_dependency_options = test_dependency_options
        self.ecdf_options = ecdf_options
