from p_value_processing.p_value_sequence import PValueSequence


class SequenceAccumulator:
    def __init__(self):
        self._seq = []

    def add_sequence(self, seq: PValueSequence):
        self._seq.append(seq)

    def get_all_sequences(self):
        return list(self._seq)
