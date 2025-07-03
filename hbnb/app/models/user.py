from app.models.base import BaseModel
import re
from app.persistence.repository import db

class User(BaseModel):
    # def __init__(self):
    #     super().__init__()

    #     # self.first_name = first_name
    #     # self.last_name = last_name
    #     # self.email = email
    #     # self.is_admin = is_admin
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)


# Set up relations later when other models have been implemented