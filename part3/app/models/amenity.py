from .base_model import BaseModel
from app import db
from sqlalchemy import Column, Integer, String


class Amenity(BaseModel):

    __tablename__ = 'amenities'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        """
        Définit le nom de l'amenity en vérifiant qu'il soit une chaîne non vide et de longueur max 50.
        """
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if not value:
            raise ValueError("name cannot be empty")
        if len(value) > 50:
            raise ValueError("name must be 50 characters or less")
        self.__name = value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
              }