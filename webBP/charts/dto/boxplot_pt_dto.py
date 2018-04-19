class BoxplotPTDto:
    def __init__(self, title: str=None, sequences: list=None, test_names: dict=None):
        self.title = title
        self.sequences = sequences
        self.test_names = test_names
