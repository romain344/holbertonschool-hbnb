import re
from .base_model import BaseModel
from app.__init__ import bcrypt

class User(BaseModel):
    _emails = set()

    def __init__(self, id, first_name, last_name, password, email, is_admin=False):
        super().__init__()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        self.is_max_length('First name', value, 50)
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        self.is_max_length('Last name', value, 50)
        self.__last_name = value

    @property
    def password(self):
        return None

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        self.__password = bcrypt.generate_password_hash(value).decode('utf-8')
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.__password, password)

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        self.is_valid_email('Email', value)
        if value in User._emails:
            raise ValueError("Email already exists")

        # Supprimer l'ancien email si on en change
        if hasattr(self, "_User__email"):
            User._emails.discard(self.__email)

        self.__email = value
        User._emails.add(value)

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        self.is_boolean('is_admin', value)
        self.__is_admin = value

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }