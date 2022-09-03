#!/usr/bin/env python3

"""A module that inherits from the BaseModel class"""



from models.base_model import BaseModel


class Amenity(BaseModel):
  """A class that stores amenities to be accessed by the user"""
  name = str()
