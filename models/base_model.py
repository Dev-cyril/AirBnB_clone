#!/usr/bin/python3
"""
    A module that would serve as a base file for all other files
    and would be inherited from
"""


import uuid
from datetime import datetime
from models import storage


class BaseModel():
    """A base model class
        responsible for all other files for this project
    """

    def __init__(self, *args, **kwargs):
        """Instantiation of attributes"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)
        else:
            if len(kwargs) != 0 and key != '__class__':
                for key, value in kwargs.items():
                    if key in ('created_at', 'updated_at'):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)

    def __str__(self):
        """String representation of the module"""
        return ('[{}] ({}) {}'.format(type(self).__name__,
                self.id, self.__dict__))

    def save(self):
        """updates the public instance attribute updated_at
            with the current datetime
        """

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values
            of __dict__ of the instance
        """
        dict_1 = self.__dict__.copy()
        dict_1["__class__"] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if key in ("created_at", "updated_at"):
                value = self.__dict__[key].isoformat()
                dict_1[key] = value
        return dict_1
