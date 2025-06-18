#!/usr/bin/python3

from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name=None):
        super().__init__()

        self.name = name

    #Getter @ setter
    # @property
    # def name(self):
    #     """returns value of amenity name"""
    #     return self._name
    
    # @name.setter
    # def name(self, value):
    #     """setter for amenity name"""
        #value has to be 50 characters only
    #     is_valid_name = 0 < len(value.strip()) <= 50
    #     if is_valid_name:
    #         self._name = value.strip()
    #     else:
    #         raise ValueError("Invalid amenity's name length!")
