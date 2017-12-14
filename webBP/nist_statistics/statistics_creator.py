from os.path import join, dirname, abspath, exists

from os import makedirs, linesep

from logger import Logger
from managers.filemanager import FileManager
from managers.groupmanager import GroupManager
from managers.nisttestmanager import NistTestManager
from managers.resultsmanager import ResultsManager
from nist_statistics.line_generator import LineGenerator
from common.my_fs_manager import MyFSManager
from nist_statistics.p_vals_processor import PValsProcessor
from nist_statistics.test_converter import TestConverter


class StatisticsCreator:
    def __init__(self, pool, config_storage):
        self.pool = pool
        self.logger = Logger()
        self.config_storage = config_storage

        this_dir = dirname(abspath(__file__))
        with open(join(this_dir, 'templates', 'template1.txt'), 'r') as f:
            self.template1 = f.read()
        with open(join(this_dir, 'templates', 'template2.txt'), 'r') as f:
            self.template2 = f.read()
        self.template2 = self.template2[:-1]
        with open(join(this_dir, 'templates', 'template3.txt'), 'r') as f:
            self.template3 = f.read()
        self.group_dao = GroupManager(self.pool)
        self.file_dao = FileManager(self.pool)
        self.results_dao = ResultsManager(self.pool)
        self.nist_dao = NistTestManager(self.pool)
        self.p_value_counter = PValsProcessor()
        self.my_fs_mgr = MyFSManager()
        self.line_generator = LineGenerator()
        self.test_converter = TestConverter()

    def compute_statistics(self, group_id, user_id):
        tests = self.group_dao.get_tests_for_group(group_id)
        my_dict = self.test_converter.get_tests_for_files(tests)
        for file_id, tests_arr in my_dict.items():
            file = self.file_dao.get_file_by_id(file_id)
            file_name = self.prepare_file(group_id, user_id, file)
            for test in tests_arr:
                self.append_lines_for_test(file_name, test)
        self.group_dao.set_statistics_computed(group_id)

    def prepare_file(self, group_id, user_id, file):
        dir_name = join(self.config_storage.path_to_users_dir, str(user_id), self.config_storage.groups, str(group_id))
        if not exists(dir_name):
            makedirs(dir_name)
        file_name = 'grp_' + str(group_id) + '_f_' + str(file.id)
        file_loc = join(dir_name, file_name)
        to_write = self.template1 + self.template2 + ' <' + file.name + '>\n' + self.template3
        with open(file_loc, 'w') as f:
            f.write(to_write)
        return file_loc

    def append_lines_for_test(self, file_name, test):
        path = self.results_dao.get_path_for_test(test)
        files = self.my_fs_mgr.get_data_files_in_dir(path)
        test_name = self.nist_dao.get_nist_param_for_test(test).get_test_name()
        for file in files:
            self.p_value_counter.reset()
            self.p_value_counter.process_p_vals_in_file(file)
            test_stats = self.p_value_counter.generate_test_statistics_obj(test_name)
            line = self.line_generator.generate_line_from_test_statistics(test_stats)
            with open(file_name, 'a') as f:
                f.write(line)
                f.write(linesep)  # write a new line
        return
