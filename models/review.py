#!/usr/bin/python3
from models.base_model import BaseModel
"""class"""


class Review(BaseModel):
    """represents the review"""
    place_id = ""
    user_id = ""
    text = ""
