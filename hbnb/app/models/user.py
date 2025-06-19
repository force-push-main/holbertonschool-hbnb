from app.models.base import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name=None, last_name=None, email=None, is_admin=False):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin


# Set up relations later when other models have been implemented