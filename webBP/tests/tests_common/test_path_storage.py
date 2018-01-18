from os import makedirs, remove
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from common.path_storage import PathStorage

this_dir = dirname(abspath(__file__))
working_dir = abspath(join(this_dir, 'working_dir_path_storage'))


class TestPathStorage(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.path_storage = PathStorage()

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_add_none_path(self):
        with self.assertRaises(TypeError) as context:
            self.path_storage.add_path(None)
            self.assertEqual('Path is None' in str(context.exception))

    def test_add_one_path(self):
        path = '/home/path/to/file.txt'
        self.path_storage.add_path(path)
        self.assertEqual([path], self.path_storage.get_all_paths())

    def test_add_more_paths(self):
        directory = '/home/path/to/directory'
        expected = []
        for i in range(0, 10):
            file = directory + 'file' + str(i) + '.txt'
            expected.append(file)
            self.path_storage.add_path(file)

        self.assertEqual(expected, self.path_storage.get_all_paths())

    def test_delete_files_on_paths(self):
        expected = []
        for i in range(0, 10):
            file = join(working_dir, 'file' + str(i) + '.txt')
            expected.append(file)
            self.path_storage.add_path(file)
            open(file, 'a').close()
            self.assertTrue(exists(file))
        remove(join(working_dir, 'file5.txt'))

        self.path_storage.delete_files_on_paths()

        for i in range(0, 5):
            file = join(working_dir, 'file' + str(i) + '.txt')
            self.assertFalse(exists(file))
        for i in range(6, 10):
            file = join(working_dir, 'file' + str(i) + '.txt')
            self.assertFalse(exists(file))



