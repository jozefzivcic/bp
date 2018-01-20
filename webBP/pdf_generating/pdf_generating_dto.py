class PdfGeneratingDto:
    def __init__(self, alpha: float=0.01, test_ids: list=None, chart_types: list=None, language: str=None,
                 output_filename: str=None):
        self.alpha = alpha
        self.test_ids = test_ids
        self.chart_types = chart_types
        self.language = language
        self.output_filename = output_filename
