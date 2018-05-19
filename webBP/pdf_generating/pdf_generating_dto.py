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

    def __repr__(self) -> str:
        ret = '<alpha: "{:0.6f}", test ids: "{}", chart types: "{}", language: "{}", o filename: "{}", ' \
              'hist opt: "{}", td opt: "{}", ecdf opt: "{}", bpt opt: "{}", prop opt: "{}", create_report: "{}">'\
            .format(self.alpha, repr(self.test_ids), repr(self.chart_types), self.language, self.output_filename,
                    repr(self.hist_options), repr(self.test_dependency_options), repr(self.ecdf_options),
                    repr(self.boxplot_pt_options), repr(self.prop_options), self.create_nist_report)
        return ret
