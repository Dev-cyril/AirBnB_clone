#!/usr/bin/python3
"""Unittest module: Test BaseModel Class."""

from models.base_model import BaseModel
from datetime import datetime
import unittest
import uuid
import time
import re


class TestBaseModel(unittest.TestCase):
    """Test Cases for BaseModel class."""

    def test_3_instantiation(self):
        """Tests instantiation of Base Model class."""
        o = BaseModel()
        self.assertEqual(str(type(o)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(o, BaseModel)
        self.assertTrue(issubclass(type(o), BaseModel))

    def test_3_id(self):
        """Test generated unique user ids."""
        o_list = [BaseModel().id for i in range(1000)]
        self.assertEqual(len(set(o_list)), len(o_list))

    def test_3_datetiem(self):
        """Tests if created_at and updated at are current at creation."""
        date_now = datetime.now()
        o = BaseModel()
        diff = o.updated_at - o.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = o.created_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def test_3_str(self):
        "Tests the __str__ (print) method"
        o = BaseModel()
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(str(o))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "BaseModel")
        self.assertEqual(res.group(2), o.id)
        # TODO: check for dictionary representation of __str__

    def test_3_save(self):
        """Test public instance method save()."""
        o = BaseModel()
        time.sleep(0.5)
        date_now = datetime.now()
        o.save()
        diff = o.updated_at - o.created_at
        self.assertTrue(abs(diff.total_seconds()) >= 0.5)
        diff = o.updated_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_3_to_dict(self):
        """Tests public instance method to_dict()."""

        o = BaseModel()
        o.name = "My First Model"
        o.my_number = 89
        d = o.to_dict()
        self.assertEqual(d["id"], o.id)
        self.assertEqual(d["__class__"], type(o).__name__)
        self.assertEqual(d["created_at"], o.created_at.isoformat())
        self.assertEqual(d["updated_at"], o.updated_at.isoformat())
        self.assertEqual(d["name"], o.name)
        self.assertEqual(d["my_number"], o.my_number)
