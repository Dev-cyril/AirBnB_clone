#!/usr/bin/env python3
"""A module that inhwerits from the BaseModel class"""


from models.base_model import BaseModel


class User(BaseModel):
    """A class that stores profiles of users"""
    email = str()
    password = str()
    first_name = str()
    last_name = str()
