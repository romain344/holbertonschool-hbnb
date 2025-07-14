from app.models.base_model import BaseModel
from .place import Place
from .user import User
from app import db
from sqlalchemy import Column, Integer, String, Float

class Review(BaseModel):

    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    description = Column(String(512), nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    # verifie qui à bein le texte
    def text(self):
        return self.__text
    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("manque le texte")
        self.__text = value

    @property
    # verifie que la note est un nombre entre 1 et 5
    def rating(self):
        return self.__rating
    @rating.setter
    def rating(self, value):
        if not isinstance(value, (int, self)):
            raise TypeError("la note doit être un nombre")
        if not (1 <= value <= 5):
            raise ValueError("la note doit être entre 1 et 5")
        self.__rating = value

    @property
    # verifie que leix lieu exeiste pour la revue
    def place(self):
        return self.__place
    @place.setter
    def place(self, value):
        if not value:
            raise ValueError("manque le lieu")
        self.__place = value

    @property
    # verifie que l'utilisateur existe pour la revue
    def user(self):
        return self.__user
    @user.setter
    def user(self, value):
        if not value:
            raise ValueError("manque l'utilisateur")
        self.__user = value