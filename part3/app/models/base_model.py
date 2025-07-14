from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Sauvegarder dans la BDD"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Supprimer de la BDD"""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Met à jour les attributs avec les valeurs d’un dictionnaire"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Convertit l’objet SQLAlchemy en dictionnaire pour JSON/API"""
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    # valide 
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