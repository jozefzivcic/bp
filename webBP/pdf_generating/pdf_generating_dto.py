from pdf_generating.options.boxplot_pt_options import BoxplotPTOptions
from pdf_generating.options.ecdf_options import EcdfOptions
from pdf_generating.options.hist_options import HistOptions
from pdf_generating.options.prop_options import PropOptions
from pdf_generating.options.test_dependency_options import TestDependencyOptions


class PdfGeneratingDto:
    def __init__(self, alpha: float=0.01, test_ids: list=None, chart_types: list=None, language: str=None,
                 output_filename: str=None, hist_options: HistOptions=None,
                 test_dependency_options: TestDependencyOptions=None,
                 ecdf_options: EcdfOptions=None, boxplot_pt_options: BoxplotPTOptions=None,
                 prop_options: PropOptions=None, create_nist_report: bool=False):
        self.alpha = alpha
        self.test_ids = test_ids
        self.chart_types = chart_types
        self.language = language
        self.output_filename = output_filename
        self.hist_options = hist_options
        self.test_dependency_options = test_dependency_options
        self.ecdf_options = ecdf_options
        self.boxplot_pt_options = boxplot_pt_options
        self.prop_options = prop_options
        self.create_nist_report = create_nist_report
