#!/usr/bin/env python3
"""A module that inherits from the BaseModel class"""


from models.base_model import BaseModel


class Review (BaseModel):
  """A class that creates reviews"""
  place_id = str()
  user_id = str()
  text = str()
