from p_value_processing.sequence_accumulator import SequenceAccumulator


class TestDependencyDto:
    def __init__(self, seq_accumulator: SequenceAccumulator=None, title: str=None):
        self.seq_accumulator = seq_accumulator
        self.title = title
