from managers.connectionpool import ConnectionPool
from managers.resultsmanager import ResultsManager


class ChartsCreator:
    def __init__(self, pool: ConnectionPool):
        self._tests_with_dirs = None
        self._results_dao = ResultsManager(pool)

    def create_line_charts_for_tests(self, test_ids: list):
        self.load_tests_with_dirs(test_ids)

    def load_tests_with_dirs(self, test_ids):
        if self._tests_with_dirs is None:
            self._tests_with_dirs = self._results_dao.get_paths_for_test_ids(test_ids)

    def reset(self):
        self._tests_with_dirs = None
