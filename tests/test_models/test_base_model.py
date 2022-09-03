#!/usr/bin/python3
"""Unittest module: Test BaseModel Class."""

from models.base_model import BaseModel
from datetime import datetime
import unittest
import uuid
import time
import re
import json


class TestBaseModel(unittest.TestCase):
    """Test Cases for BaseModel class."""

    def test_3_init_no_args(self):
        """Tests __init__ with no arguments."""
        with self.assertRaises(TypeError) as e:
            BaseModel.__init__()
        msg = "BaseModel.__init__() missing 1 required positional \
argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_4_init_many_args(self):
        """Tests __init__ with many arguments."""
        args = [i for i in range(1000)]
        o = BaseModel(*args)

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

    def test_3_datetime(self):
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
        s_dict = res.group(3)
        s_dict = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s_dict)
        d = json.loads(s_dict.replace("'", '"'))
        d2 = o.__dict__.copy()
        d2["created_at"] = repr(d2["created_at"])
        d2["updated_at"] = repr(d2["updated_at"])
        self.assertEqual(d, d2)

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

    def test_3_to_dict_no_args(self):
        """Tests to_dict() with no arguments."""
        with self.assertRaises(TypeError) as e:
            BaseModel.to_dict()
        msg = "BaseModel.to_dict() missing 1 required positional \
argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_3_to_dict_excess_args(self):
        """Tests to_dict() with many arguments."""
        with self.assertRaises(TypeError) as e:
            BaseModel.to_dict(self, 98)
        msg = "BaseModel.to_dict() takes 1 positional argument \
but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def test_4_instantiation(self):
        """Tests instantiation with **kwargs."""
        my_model = BaseModel()
        my_model.name = "My_First_Model"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual(my_new_model.to_dict(), my_model.to_dict())

    def test_4_instantiation_dict(self):
        """Tests instantiation with **kwargs from custom dict."""
        d = {"__class__": "BaseModel",
             "updated_at":
             datetime(2012, 12, 31, 12, 34, 56, 12345).isoformat(),
             "created_at": datetime.now().isoformat(),
             "id": uuid.uuid4(),
             "var": "foobar",
             "int": 108,
             "float": 3.14}
        o = BaseModel(**d)
        self.assertEqual(o.to_dict(), d)
