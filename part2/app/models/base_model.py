import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    # ✅ Méthodes de validation à utiliser depuis les classes enfants
    def is_max_length(self, field_name, value, max_len):
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")
        if len(value) > max_len:
            raise ValueError(f"{field_name} cannot exceed {max_len} characters.")

    def is_valid_email(self, field_name, email):
        if not isinstance(email, str):
            raise TypeError(f"{field_name} must be a string.")
        if "@" not in email or "." not in email:
            raise ValueError(f"{field_name} must be a valid email address.")

    def is_boolean(self, field_name, value):
        if not isinstance(value, bool):
            raise ValueError(f"{field_name} must be a boolean.")