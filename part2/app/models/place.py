from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, longitude, latitude, price, owner_id, amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.longitude = longitude
        self.latitude = latitude
        self.price = price
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = amenities if amenities is not None else []

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Title must be a non-empty string.")
        self.__title = value

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
    def owner_id(self):
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Owner ID must be a non-empty string.")
        self.__owner_id = value
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [a.id for a in self.amenities]
        }