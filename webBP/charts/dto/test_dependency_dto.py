from enums.filter_uniformity import FilterUniformity
from p_value_processing.sequence_accumulator import SequenceAccumulator


class TestDependencyDto:
    def __init__(self, alpha: float=0.01, filter_unif: FilterUniformity=FilterUniformity.REMOVE_NON_UNIFORM,
                 seq_accumulator: SequenceAccumulator=None, title: str=None):
        self.alpha = alpha
        self.filter_unif = filter_unif
        self.seq_accumulator = seq_accumulator
        self.title = title
