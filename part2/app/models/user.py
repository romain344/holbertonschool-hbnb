import re
from app.models.base_model import BaseModel

class User(BaseModel):
    _emails = set()

    def __init__(self, first_name, last_name, password, email, is_admin=False):
        super().__init__()
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
        return self.__password

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        self.__password = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        self.is_valid_email('Email', value)
        old_email = getattr(self, "_User__email", None)
    # Si c'est le même email qu'avant, ne rien faire
        if old_email == value:
            return
    # Sinon, vérifier s'il est déjà utilisé
        if value in User._emails:
            raise ValueError("Email already exists")
    # Retirer l'ancien email de l'ensemble s’il existe
        if old_email:
            User._emails.discard(old_email)
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
            "email": self.email,
            "password": self.password
        }