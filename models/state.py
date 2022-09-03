#!/usr/bin/env python3

"""A module that inherits from the BaseModel class"""



from models.base_model import BaseModel


class State(BaseModel):
  """A class that takes the state of the user"""
  
  name = str()
