import re
from base_model import BaseModel
from user import User

class Place(BaseModel):
    def __init__(self, name, description, longitude, latitude, price, owner):
        super().__init__()
        self.name = name
        self.description = description
        self.longitude = longitude
        self.latitude = latitude
        self.price = price
        self.owner = owner
        self.reviews = []
        self.amenities = []  # corrigé 'amanities' en 'amenities'
    
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Name must be a non-empty string.")
        self.__name = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Description must be a non-empty string.")
        self.__description = value

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number.")
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self.__longitude = value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number.")
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self.__latitude = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        if value < 1:
            raise ValueError("Price must be positive.")
        self.__price = value

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Owner must be a non-empty string.")
        self.__owner = value