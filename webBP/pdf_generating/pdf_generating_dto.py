class PdfGeneratingDto:
    def __init__(self, test_ids: list=None, test_types: list=None, language: str=None, output_filename: str=None):
        self.test_ids = test_ids
        self.test_types = test_types
        self.language = language
        self.output_filename = output_filename
