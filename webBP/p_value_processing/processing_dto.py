class ProcessingDto:
    def __init__(self):
        self._data = []
        self._iterable = None

    def add(self, test_id: int, directory: str):
        self._data.append((test_id, directory))

    def __iter__(self):
        self._iterable = iter(self._data)
        return self._iterable

    def __next__(self):
        return next(self._iterable)

    def empty(self):
        return not self._data
