#!/usr/bin/python3
"""unittest for base_model"""


import datetime
import unittest
from models.base_model import BaseModel


class TestModels(unittest.TestCase):
    """Test cases for all models"""

    def setUp(self):
        """
            Initializing instance with width and height
            parameters
        """
        self.r = BaseModel(5)

    def tearDown(self):
        """
            Deleting created instance
        """
        del self.r

    def test_id(self):
        """test for id uniqueness"""
        r1 = BaseModel(6)
        r2 = BaseModel(4)
        self.assertEqual(type(r1.id), str)
        self.assertEqual(r1.id == r2.id, False)

    def test_time(self):
        """test cases for time instances"""
        r1 = BaseModel()
        self.assertEqual(type(r1.created_at), datetime.datetime)
        self.assertEqual(r1.created_at == r1.updated_at, True)

    def test_string(self):
        """test for __str__ method"""
        r1 = BaseModel(8)
        self.assertEqual('[BaseModel] ({}) {}'.format(r1.id, r1.__dict__),
                         r1.__str__())

    def test_save(self):
        """test for save method"""
        self.assertEqual(self.r.save() != self.r.created_at, True)

    def test_to_dict(self):
        """test for to_dict method"""
        r1 = self.r.to_dict()
        self.assertEqual(r1, {'__class__': 'BaseModel',
                              'created_at': self.r.created_at.isoformat(),
                              'id': self.r.id,
                              'updated_at': self.r.updated_at.isoformat()})


if __name__ == '__main__':
    unittest.main()
