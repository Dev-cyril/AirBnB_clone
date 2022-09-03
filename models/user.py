#!/usr/bin/python3
"""Module user
Describes a User with its various attributes."""

from models.base_model import BaseModel


class User(BaseModel):
    """Represents a User."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
