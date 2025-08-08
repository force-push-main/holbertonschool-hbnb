from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from app.persistence.repository import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    places = relationship("Place", secondary="place_amenity", back_populates="amenities")
