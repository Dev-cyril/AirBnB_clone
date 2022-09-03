#!/usr/bin/python3
"""Unittest module: Test User Class."""

from models.base_model import BaseModel
from models.user import User
import unittest
import uuid


class TestUser(unittest.TestCase):
    """Test Cases for User class."""