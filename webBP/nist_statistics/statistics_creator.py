import math
from os import linesep

from os.path import join, dirname, abspath, exists

from common.my_fs_manager import MyFSManager
from common.test_converter import TestConverter
from enums.nist_test_type import NistTestType
from logger import Logger
from managers.dbtestmanager import DBTestManager
from managers.filemanager import FileManager
from managers.groupmanager import GroupManager
from managers.nisttestmanager import NistTestManager
from managers.resultsmanager import ResultsManager
from models.file import File
from models.nistparam import NistParam
from nist_statistics.line_generator import LineGenerator
from nist_statistics.p_vals_processor import PValsProcessor


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
        self.test_dao = DBTestManager(self.pool)
        self.group_dao = GroupManager(self.pool)
        self.file_dao = FileManager(self.pool)
        self.results_dao = ResultsManager(self.pool)
        self.nist_dao = NistTestManager(self.pool)
        self.p_value_counter = PValsProcessor()
        self.my_fs_mgr = MyFSManager()
        self.line_generator = LineGenerator()
        self.test_converter = TestConverter()
        self.tests_in_file = [0 for _ in range(15)]
        self.general_sample_size = 0
        self.random_excursion_sample_size = 0

    def compute_statistics(self, group_id: int, directory: str, alpha: float=0.01) -> dict:
        tests = self.group_dao.get_tests_for_group(group_id)
        ret = self.create_stats_for_tests(tests, directory, alpha)
        self.group_dao.set_statistics_computed(group_id)
        return ret

    def create_stats_for_tests_ids(self, test_ids: list, directory: str, alpha: float=0.01) -> dict:
        tests = self.test_dao.get_tests_by_id_list(test_ids)
        return self.create_stats_for_tests(tests, directory, alpha)

    def create_stats_for_tests(self, tests: list, directory: str, alpha: float=0.01) -> dict:
        my_dict = self.test_converter.get_tests_for_files(tests)
        file_paths = {}
        for file_id, tests_arr in my_dict.items():
            self.reset()
            file = self.file_dao.get_file_by_id(file_id)
            file_name = self.prepare_file(directory, tests_arr[0].id, file)
            for test in tests_arr:
                self.append_lines_for_test(file_name, test)
            self.append_end(file_name, alpha)
            file_paths[file_id] = file_name
        return file_paths

    def prepare_file(self, directory: str, test_id: int, file: File) -> str:
        if not exists(directory):
            raise RuntimeError('Given directory {} does not exists'.format(directory))
        file_name = 'report_for_file_id_{}_and_first_test_id_{}.txt'.format(file.id, test_id)
        file_loc = join(directory, file_name)
        to_write = self.template1 + self.template2 + ' <' + file.name + '>\n' + self.template3
        with open(file_loc, 'w') as f:
            f.write(to_write)
        return file_loc

    def append_lines_for_test(self, file_name, test):
        path = self.results_dao.get_path_for_test(test)
        files = self.my_fs_mgr.get_data_files_in_dir(path)
        nist_param = self.nist_dao.get_nist_param_for_test(test)
        self.add_test_for_file(nist_param)
        test_name = nist_param.get_test_name()
        for file in files:
            self.p_value_counter.reset()
            self.p_value_counter.process_p_vals_in_file(file)
            test_stats = self.p_value_counter.generate_test_statistics_obj(test_name)
            if nist_param.is_test_type(NistTestType.TEST_RND_EXCURSION):
                self.random_excursion_sample_size = test_stats.sample_size
            line = self.line_generator.generate_line_from_test_statistics(test_stats)
            with open(file_name, 'a') as f:
                f.write(line)
                f.write(linesep)  # write a new line
        self.general_sample_size = nist_param.streams

    def append_end(self, file_name: str, alpha: float):
        to_write = '\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n'
        case1 = False
        case2 = False
        if self.contains_test(NistTestType.TEST_RND_EXCURSION) \
                or self.contains_test(NistTestType.TEST_RND_EXCURSION_VAR):
            case2 = True
        for t_type in NistTestType:
            if self.contains_test(t_type) and (t_type != NistTestType.TEST_RND_EXCURSION) and \
                    (t_type != NistTestType.TEST_RND_EXCURSION_VAR):
                case1 = True
                break
        if case1:
            if self.general_sample_size == 0:
                to_write += 'The minimum pass rate for each statistical test with the exception of the\n'
                to_write += 'random excursion (variant) test is undefined.\n\n'
            else:
                pass_rate = (1.0 - alpha) - 3.0 * math.sqrt((alpha * (1.0 - alpha)) / float(self.general_sample_size))
                to_write += 'The minimum pass rate for each statistical test with the exception of the\n'
                to_write += 'random excursion (variant) test is approximately = {0:.6f} for a\n' \
                    .format(pass_rate if self.general_sample_size else 0.0)
                to_write += 'sample size = {0:d} binary sequences.\n\n'.format(self.general_sample_size)
        if case2:
            if self.random_excursion_sample_size == 0:
                to_write += 'The minimum pass rate for the random excursion (variant) test is undefined.\n\n'
            else:
                pass_rate = (1.0 - alpha) - 3.0 * math.sqrt((alpha * (1.0 - alpha)) /
                                                            float(self.random_excursion_sample_size))
                to_write += 'The minimum pass rate for the random excursion (variant) test\n'
                to_write += 'is approximately {0:.6f} for a sample size = {1:d} binary sequences.\n\n' \
                    .format(pass_rate, self.random_excursion_sample_size)
        to_write += 'For further guidelines construct a probability table using the MAPLE program\n'
        to_write += 'provided in the addendum section of the documentation.\n'
        to_write += '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
        with open(file_name, 'a') as f:
            f.write(to_write)

    def add_test_for_file(self, nist_param: NistParam):
        index = nist_param.test_number - 1
        self.tests_in_file[index] += 1

    def reset(self):
        self.tests_in_file = [0 for _ in range(15)]
        self.general_sample_size = 0
        self.random_excursion_sample_size = 0

    def contains_test(self, test_type: NistTestType):
        index = test_type.value - 1
        return self.tests_in_file[index] > 0
