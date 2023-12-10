#!/usr/bin/python3
"""File storage"""
# models/engine/file_storage.py

import json
from os.path import exists
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.user import User

class FileStorage:
    """File Storage"""
    __file_path = "file.json"
    __objects = {}
    clss = {"BaseModel": BaseModel, "User": User, "Place": Place,
             "Amenity": Amenity, "City": City, "Review": Review,
             "State": State}

    def all(self):
        """Return objects."""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        ser_obj = {}
        for key, obj in FileStorage.__objects.items():
            ser_obj[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as json_file:
            json.dump(ser_obj, json_file)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, encoding="utf-8") as json_file:
                deserialized_file = json.load(json_file)
                for values in deserialized_file.values():
                    cls = values["__class__"]
                    if isinstance(cls, str) and type(eval(cls)) == type:
                        self.new(eval(cls)(**values))
        except FileNotFoundError:
            pass
