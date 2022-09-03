#!/usr/bin/env python3
"""A module that inherits from the BaseModel class"""


from models.base_model import BaseModel

class City(BaseModel):
  """A class that takes rhe city of the user"""
  name = str()
  state_id = str()
