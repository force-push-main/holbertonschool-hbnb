from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from app.persistence.repository import db

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(128), nullable=False)

    places = relationship('Place', back_populates='owner', lazy=True, cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="author", lazy=True, cascade="all, delete-orphan")

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if not password:
            raise ValueError('Password cannot be empty')
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not password:
            return False
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)