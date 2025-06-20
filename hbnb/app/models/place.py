#!/usr/bin/python3

from app.models.base import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title=None, description=None, price=None, latitude=None, longitude=None, owner=None, amenities=None):
        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = amenities or [] # List to store related amenities
        self.reviews = []

    def add_amenities(self, item):
        self.amenities.append(item)

    def add_review(self, item):
        self.reviews.append(item)

