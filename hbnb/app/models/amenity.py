#!/usr/bin/python3

from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name=None):
        super().__init__()

        self.name = name
