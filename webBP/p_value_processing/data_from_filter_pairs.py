from p_value_processing.filtered_item_dto import FilteredItemDto
from p_value_processing.p_value_sequence import PValueSequence


class DataFromFilterPairs:
    def __init__(self):
        self._kept = {}
        self._deleted = {}

    def add_kept(self, item: FilteredItemDto):
        seq = item.ds_info.p_value_sequence
        self._kept[seq] = item

    def add_deleted(self, item: FilteredItemDto):
        seq = item.ds_info.p_value_sequence
        self._deleted[seq] = item

    def get_kept(self) -> list:
        return list(self._kept.values())

    def get_deleted(self) -> list:
        return list(self._deleted.values())

    def get_kept_len(self) -> int:
        return len(self._kept)

    def get_deleted_len(self) -> int:
        return len(self._deleted)

    def get_kept_by_seqcs(self, seq1: PValueSequence, seq2: PValueSequence) -> FilteredItemDto:
        return self._kept[(seq1, seq2)]

    def get_deleted_by_seqcs(self, seq1: PValueSequence, seq2: PValueSequence) -> FilteredItemDto:
        return self._deleted[(seq1, seq2)]

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self._kept == other._kept and self._deleted == other._deleted
