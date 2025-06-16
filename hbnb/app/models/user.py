from app.models.base import BaseModel
import re


EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def validate_string(value, field):
    if not value:
        raise ValueError(f"{field} must contain text")
    if type(value) != str:
        raise TypeError(f"{field} must be a string")


class User(BaseModel):
    def __init__(self, first_name=None, last_name=None, email=None, is_admin=False):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self.first_name

    @first_name.setter
    def first_name(self, value):
        validate_string(value, 'first_name')
        if len(value) > 50:
            raise ValueError("first_name must be less than 50 characters")
        self.first_name = value

    @property
    def last_name(self):
        return self.last_name

    @last_name.setter
    def last_name(self, value):
        validate_string(value, 'last_name')
        if len(value) > 50:
            raise ValueError("last_name must be less than 50 characters")
        self.last_name = value

    @property
    def email(self):
        return self.email

    @email.setter
    def email(self, value):
        validate_string(value, 'email')
        if re.match(EMAIL_REGEX, value):
            raise ValueError("email must be a valid email address")
        self.email = value

    @property
    def is_admin(self):
        return self.is_admin

    @is_admin.setter
    def is_admin(self, value):
        if type(value) != bool:
            raise TypeError("is_admin must be a boolean")
        self.is_admin = value


# Set up relations later when other models have been implemented
