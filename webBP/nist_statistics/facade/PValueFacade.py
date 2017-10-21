import json

from managers.resultsmanager import ResultsManager
from nist_statistics.my_fs_manager import MyFSManager
from nist_statistics.p_value_counter import PValueCounter
from models.test import Test


class PValueFacade:
    def __init__(self, pool, alpha=0.01):
        self.alpha = alpha
        self.results_dao = ResultsManager(pool)
        self.fs_mgr = MyFSManager()

    def get_json_p_value_intervals_for_test(self, test: Test):
        path = self.results_dao.get_path_for_test(test)
        if path is None:
            return None
        results_file = self.fs_mgr.get_results_file_in_dir(path)
        if results_file is None:
            return None

        p_value_counter = PValueCounter()
        p_value_counter.count_p_values_in_file(results_file)
        arr = p_value_counter.arr
        data = {'data': []}
        temp = data['data']

        for i in range(0, 9):
            interval = '[0.' + str(i) + ', 0.' + str(i + 1) + ')'
            temp.append([interval, arr[i]])
        interval = '[0.9, 1.0]'
        temp.append([interval, arr[9]])

        return json.dumps(data)
