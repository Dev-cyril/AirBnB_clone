#!/usr/bin/python3
"""Unittest for file_storage.py"""

from models.engine.file_storage import FileStorage as e
import models
import unittest


class TestFileStorage(unittest.TestCase):
    """test cases for FileStorage instance methods"""
    def test_class_instances(self):
        """test for class instance attributes"""
        self.assertFalse(hasattr(e, '__objects'))
        self.assertFalse(hasattr(e, '__file_path'))

    def test_all_method(self):
        """test for all method that returns the obj"""
        self.assertEqual(len(e.all(e)) > 0, True)
        with self.assertRaises(TypeError) as f:
            e.all(e, 4)
        errMsg = 'FileStorage.all() takes 1 positional argument but 2 were given'
        self.assertEqual(str(f.exception), errMsg)

    def test_save_method(self):
        """
            test for save method
            tests if the dictionary object is serialized into the json file
        """
        with open('file.json') as f:
            self.assertEqual(type(f.read()) == str, True)

    def test_init_without_arg(self):
        """Tests initialization without args"""
        self.assertEqual(type(e()), e)

    def test_init_with_arg(self):
        """Tests initialization with args"""
        with self.assertRaises(TypeError):
            e(None)

    def test_storage_initialization(self):
        """Tests storage created in __init__.py"""
        self.assertEqual(type(models.storage), e)


if __name__ == '__main__':
    unittest.main()