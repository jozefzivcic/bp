from managers.resultsmanager import ResultsManager
from models.test import Test
from nist_statistics.my_fs_manager import MyFSManager


class PValueProvider:
    def __init__(self, pool):
        self.result_dao = ResultsManager(pool)
        self.fs_manager = MyFSManager()

    def get_p_values_for_test(self, test: Test):
        path_to_results = self.result_dao.get_path_for_test(test)
        if path_to_results is None:
            return None
        files = self.fs_manager.get_data_files_in_dir(path_to_results)
        if files is None:
            return None
        arr = []
        for file in files:
            self.append_p_values_from_file(file, arr)
        return arr

    def append_p_values_from_file(self, file: str, arr: list):
        with open(file, 'r') as f:
            for line in f:
                arr.append(float(line))
