class TestConverter:
    def get_tests_for_files(self, arr):
        """
        Converts array of tests into dictionary. This dictionary contains id's of files as keys. For each key,
        there is an array of tests, that are associated with the file - i.e. tests which have tests.id_file the same as
        files.id in database.
        :param arr: Array of tests
        :return: Dictionary of file_ids and associated tests.
        """
        my_dict = {}
        for test in arr:
            if test.file_id in my_dict:
                my_dict[test.file_id].append(test)
            else:
                my_dict[test.file_id] = [test]
        return my_dict