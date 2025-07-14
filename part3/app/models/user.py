from .base_model import BaseModel, db
from app import bcrypt
from sqlalchemy.orm import validates

class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    _password_hash = db.Column("password", db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, password, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.password = password  # utilise le setter ici
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        self._password_hash = bcrypt.generate_password_hash(value).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def get_password_hash(self):
        return self._password_hash

    @validates('first_name')
    def validate_first_name(self, key, value):
        self.is_max_length('First name', value, 50)
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        self.is_max_length('Last name', value, 50)
        return value

    @validates('email')
    def validate_email(self, key, value):
        self.is_valid_email('Email', value)
        return value

    @validates('is_admin')
    def validate_is_admin(self, key, value):
        self.is_boolean('is_admin', value)
        return value

    def to_dict(self):
        """Retourne un dictionnaire sans le mot de passe"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }