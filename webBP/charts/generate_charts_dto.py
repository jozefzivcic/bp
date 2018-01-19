class GenerateChartsDto:
    def __init__(self, test_ids: list, chart_types: dict, directory: str):
        self.test_ids = test_ids
        self.chart_types = chart_types
        self.directory = directory
