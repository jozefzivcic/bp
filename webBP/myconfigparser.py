import io
import re


class MyConfigParser:
    def __init__(self):
        """
        Initializes dictionary.
        """
        self._dict = {}

    def reset(self):
        """
        Removes all key-value pairs from this object.
        """
        self._dict.clear()

    def parse_file(self, file):
        """
        Parses input file. Input file must have following structure:
            comments begin with # (hash) as first character on the line,
            records are formed as key=value.
        :param file: Path to file, that is to be parsed.
        :return: If file has wrong structure then False, True otherwise.
        """
        with io.open(file, mode='r', encoding='utf-8') as file_handle:
            tempDict = {}
            for line in file_handle:
                if line[0] == '#' or line == '\n':
                    continue
                res = re.search(r'^(.+[^\\])[=](.+)$', line)
                if not res:
                    return False
                groups = res.groups()
                if not groups:
                    return False
                tempDict[groups[0]] = groups[1]
            self._dict = tempDict
            return True

    def return_key_and_values(self):
        """
        Returns content of attribute _dict.
        :return: Copy of attribute _dict.
        """
        temp_dict = self._dict.copy()
        return temp_dict

    def get_key(self, key):
        """
        Returns value associated to the key.
        :param key: Key, which value is returned.
        :return: Value of key, that is given as an attribute.
        """
        return self._dict[key]
