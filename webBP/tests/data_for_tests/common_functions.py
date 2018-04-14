from os.path import join, dirname, abspath

from models.file import File
from models.nistparam import NistParam
from models.test import Test
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import FileIdData, UserIdData, TestsIdData, dict_for_test_13, dict_for_test_14, \
    dict_for_test_41, dict_for_test_42, dict_for_test_43

this_dir = dirname(abspath(__file__))
sample_files_dir = abspath(join(this_dir, '..', 'sample_files_for_tests'))
path_to_tests_results = join(sample_files_dir, 'users', '4', 'tests_results')


def get_file_by_id(file_id: int):
    file = File()
    file.id = file_id
    file.user_id = UserIdData.user1_id
    file.hash = 'ABCD_' + str(file_id)
    file.file_system_path = '/home/this/is/non/existing/path/' + str(file_id)
    if file_id == FileIdData.file1_id:
        file.name = 'First file'
        return file
    elif file_id == FileIdData.file2_id:
        file.name = 'Second file'
        return file
    elif file_id == FileIdData.file3_id:
        file.name = 'Third_file'
        return file
    raise ValueError('File id ' + str(file_id) + ' is unsupported')


def results_dao_get_paths_for_test_ids(test_ids: list) -> list:
    ret = []
    if TestsIdData.test1_id in test_ids:
        ret.append((TestsIdData.test1_id, join(path_to_tests_results, str(TestsIdData.test1_id))))
    if TestsIdData.test2_id in test_ids:
        ret.append((TestsIdData.test2_id, join(path_to_tests_results, str(TestsIdData.test2_id))))
    if TestsIdData.test3_id in test_ids:
        ret.append((TestsIdData.test3_id, join(path_to_tests_results, str(TestsIdData.test3_id))))
    if TestsIdData.test4_id in test_ids:
        ret.append((TestsIdData.test4_id, join(path_to_tests_results, str(TestsIdData.test4_id))))
    if TestsIdData.test5_id in test_ids:
        ret.append((TestsIdData.test5_id, join(path_to_tests_results, str(TestsIdData.test5_id))))
    return ret


def result_dao_get_path_for_test(test: Test) -> list:
    ret = results_dao_get_paths_for_test_ids([test.id])
    return ret[0][1]


def db_test_dao_get_tests_by_id_list(test_ids: list) -> list:
    ret = []
    if TestsIdData.test1_id in test_ids:
        ret.append(db_test_dao_get_test_by_id(TestsIdData.test1_id))
    if TestsIdData.test2_id in test_ids:
        ret.append(db_test_dao_get_test_by_id(TestsIdData.test2_id))
    if TestsIdData.test3_id in test_ids:
        ret.append(db_test_dao_get_test_by_id(TestsIdData.test3_id))
    if TestsIdData.test4_id in test_ids:
        ret.append(db_test_dao_get_test_by_id(TestsIdData.test4_id))
    if TestsIdData.test5_id in test_ids:
        ret.append(db_test_dao_get_test_by_id(TestsIdData.test5_id))
    return ret


def db_test_dao_get_test_by_id(test_id: int) -> Test:
    test = Test()
    test.id = test_id
    test.test_table = 'nist'
    if TestsIdData.test1_id == test_id:
        test.file_id = FileIdData.file1_id
        return test
    if TestsIdData.test2_id == test_id:
        test.file_id = FileIdData.file1_id
        return test
    if TestsIdData.test3_id == test_id:
        test.file_id = FileIdData.file1_id
        return test
    if TestsIdData.test4_id == test_id:
        test.file_id = FileIdData.file2_id
        return test
    if TestsIdData.test5_id == test_id:
        test.file_id = FileIdData.file2_id
        return test
    if TestsIdData.non_existing_test_id == test_id:
        test.test_table = 'something'
        test.file_id = FileIdData.file1_id
        return test
    raise ValueError('Test id ' + str(test_id) + ' is unsupported')


def nist_dao_get_nist_param_for_test(test: Test) -> NistParam:
    param = NistParam()
    param.test_id = test.id
    param.streams = 10
    if TestsIdData.test1_id == test.id:
        param.test_number = 1
        return param
    if TestsIdData.test2_id == test.id:
        param.test_number = 3
        return param
    if TestsIdData.test3_id == test.id:
        param.test_number = 14
        return param
    if TestsIdData.test4_id == test.id:
        param.test_number = 15
        return param
    if TestsIdData.test5_id == test.id:
        param.test_number = 5
        return param
    raise ValueError('No NIST param for test id ' + str(test.id) + ' is unsupported')


def func_return_false(*args):
    return False


def func_return_true(*args):
    return True


def func_prepare_acc() -> PValuesAccumulator:
    dto1 = PValuesDto(dict_for_test_13)
    dto2 = PValuesDto(dict_for_test_14)
    dto3 = PValuesDto(dict_for_test_41)
    dto4 = PValuesDto(dict_for_test_42)
    dto5 = PValuesDto(dict_for_test_43)

    acc = PValuesAccumulator()
    acc.add(TestsIdData.test1_id, dto1)
    acc.add(TestsIdData.test2_id, dto2)
    acc.add(TestsIdData.test3_id, dto3)
    acc.add(TestsIdData.test4_id, dto4)
    acc.add(TestsIdData.test5_id, dto5)
    return acc
