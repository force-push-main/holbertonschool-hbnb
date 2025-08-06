#!/usr/bin/python3

from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from app.persistence.repository import db

class Review(BaseModel):
    __tablename__ = 'reviews'
<<<<<<< HEAD

    text = db.Column(db.String(512), nullable=False)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'))

    author = relationship("User", back_populates="reviews", lazy=True)
    place = relationship("Place", back_populates="reviews", lazy=True)
=======

    text = db.Column(db.String(512), nullable=False)
    rating = db.Column(db.Integer)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'))

    author = relationship("User", back_populates="reviews", lazy=True)
    place = relationship("Place", back_populates="reviews", lazy=True)
>>>>>>> origin/master
