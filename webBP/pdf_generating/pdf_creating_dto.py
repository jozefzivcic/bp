class PdfCreatingDto:
    def __init__(self, template: str=None, output_file: str=None, keys_for_template: dict={}):
        self.template = template
        self.output_file = output_file
        self.keys_for_template = keys_for_template
