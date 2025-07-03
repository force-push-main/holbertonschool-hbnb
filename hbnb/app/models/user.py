from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from app.persistence.repository import db

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship('Place', back_populates='owner', lazy=True)
    reviews = relationship("Review", back_populates="author", lazy=True)
