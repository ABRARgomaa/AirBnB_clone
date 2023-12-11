#!/usr/bin/python3
from models.base_model import BaseModel
"""class"""


class User(BaseModel):
    """represents the user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
