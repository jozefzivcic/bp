from os.path import isfile, join

from os import listdir

import re


class MyFSManager:
    def get_data_files_in_dir(self, directory, get_results_file = True):
        files = [file for file in listdir(directory) if isfile(join(directory, file))]
        if len(files) == 2 and get_results_file:
            return [join(directory, 'results.txt')]
        regex = re.compile(r'^(data)(\d+)(.txt)$')
        filtered_files = list(filter(regex.search, files))
        filtered_files = sorted(filtered_files, key=lambda x: int(regex.match(x).groups()[1]))
        full_paths = [join(directory, file) for file in filtered_files]
        return full_paths

    def get_results_file_in_dir(self, directory):
        if directory is None:
            return None
        return join(directory, 'results.txt')

    def get_files_with_p_values_in_dir(self, directory: str) -> list:
        files = self.get_data_files_in_dir(directory, False)
        results_file = join(directory, 'results.txt')
        if isfile(results_file):
            files.append(results_file)
        return files
