from p_value_processing.filtered_item_dto import FilteredItemDto


class DataFromFilterPairs:
    def __init__(self):
        self._kept = []
        self._deleted = []

    def add_kept(self, item: FilteredItemDto):
        self._kept.append(item)

    def add_deleted(self, item: FilteredItemDto):
        self._deleted.append(item)

    def get_kept(self) -> list:
        return list(self._kept)

    def get_deleted(self) -> list:
        return list(self._deleted)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self._kept == other._kept and self._deleted == other._deleted
