import io
import re

class ConfigParser:
    def __init__(self):
        self._dict = {}

    def reset(self):
        self._dict.clear()

    def parse_file(self, file):
        with io.open(file, mode='r', encoding='utf-8') as file_handle:
            tempDict = {}
            for line in file_handle:
                if line[0] == '#':
                    continue
                res = re.search(r'^(.+[^\\])[=](.+)$',line)
                if not res:
                    return False
                groups = res.groups()
                if not groups:
                    return False
                tempDict[groups[0]] = groups[1]
            self._dict = tempDict
            return True

    def return_key_and_values(self):
        temp_dict = self._dict.copy()
        return temp_dict

    def get_key(self, key):
        return self._dict[key]