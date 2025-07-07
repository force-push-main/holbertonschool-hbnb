#!/usr/bin/python3

from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from app.persistence.repository import db

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    owner = relationship('User', back_populates='places', lazy=True)
    reviews = relationship("Review", back_populates="place", lazy=True)
    amenities = relationship("Amenity", secondary="place_amenity", back_populates="places", lazy=True)


# Many-to-Many junction table
class PlaceAmenity(BaseModel):
    __tablename__ = 'place_amenity'

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), primary_key=True)
    amenity_id = db.Column(db.String(36), db.ForeignKey('amenities.id'), primary_key=True)