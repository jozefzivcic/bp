from os.path import basename, splitext

from common.my_fs_manager import MyFSManager
from p_value_processing.p_values_dto import PValuesDto


class NistLoader():
    def __init__(self):
        self._p_values_in_files = {}
        self._fs_manager = MyFSManager()

    def load_p_values_in_dir(self, directory: str):
        files = self._fs_manager.get_files_with_p_values_in_dir(directory)
        for file in files:
            file_name = self.get_file_name(file)
            self._p_values_in_files[file_name] = []
            l = self._p_values_in_files[file_name]
            with open(file, 'r') as f:
                for line in f:
                    l.append(float(line))

    def get_file_name(self, full_path: str):
        name_with_ext = basename(full_path)
        name, extension = splitext(name_with_ext)
        return name

    def generate_dto(self) -> PValuesDto:
        dto = PValuesDto(dict(self._p_values_in_files))
        return dto

    def reset(self):
        self._p_values_in_files.clear()

