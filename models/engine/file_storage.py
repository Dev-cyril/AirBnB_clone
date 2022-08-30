#!/usr/bin/python3
"""module for file storage"""


import json
from os import path
from models.base_model import BaseModel


class FileStorage():
    """
        serializes instances to a JSON file
        and deserializes JSON file to instances
    """
    __file_path = 'file.json'
    __objects = dict()

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects
            the obj with key <obj class name>.id
        """
        self.__objects['{}.{}'.format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """serializes __objects
            to the JSON file (path: __file_path)
        """
        
        with open(self.__file_path, mode='w') as f:
            dic = {key: value.to_dict() for key, value in self.__objects.items()}
            json.dump(dic, f)

    def reload(self):
        """deserializes the JSON file to __objects """
        if path.isfile(self.__file_path):
            with open(self.__file_path) as f:
                d = json.load(f)
                
