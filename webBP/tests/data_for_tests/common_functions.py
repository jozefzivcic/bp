from models.file import File
from tests.data_for_tests.common_data import FileIdData, UserIdData


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
    raise ValueError('File id ' + str(file_id) + ' is unsupported')
