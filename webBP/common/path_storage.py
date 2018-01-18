from os.path import exists

from os import remove


class PathStorage:
    def __init__(self):
        self._paths = []

    def add_path(self, path: str):
        if path is None:
            raise TypeError('Path is None')
        self._paths.append(path)

    def get_all_paths(self) -> list:
        return list(self._paths)

    def delete_files_on_paths(self):
        for file in self._paths:
            if exists(file):
                remove(file)
