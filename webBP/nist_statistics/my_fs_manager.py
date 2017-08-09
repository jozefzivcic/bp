from os.path import isfile, join

from os import listdir

import re


class MyFSManager:
    def get_data_files_in_dir(self, directory):
        files = [file for file in listdir(directory) if isfile(join(directory, file))]
        if len(files) == 2:
            return [join(directory, 'results.txt')]
        regex = re.compile(r'^(data)(\d+)(.txt)$')
        filtered_files = list(filter(regex.search, files))
        filtered_files = sorted(filtered_files, key=lambda x: int(regex.match(x).groups()[1]))
        full_paths = [join(directory, file) for file in filtered_files]
        return full_paths
