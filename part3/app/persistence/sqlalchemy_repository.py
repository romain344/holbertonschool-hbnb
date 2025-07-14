from app import db
from app.models import User, Place, Review, Amenity

class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()


class PlaceRepository:
    def __init__(self, session):
        self.session = session

    def add(self, place):
        self.session.add(place)
        self.session.commit()

    def get(self, id):
        return self.session.query(Place).get(id)

    def get_all(self):
        return self.session.query(Place).all()

    def update(self, id, data):
        place = self.get(id)
        if place:
            for key, value in data.items():
                setattr(place, key, value)
            self.session.commit()
        return place

    def delete(self, id):
        place = self.get(id)
        if place:
            self.session.delete(place)
            self.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.session.query(Place).filter(getattr(Place, attr_name) == attr_value).first()


class ReviewRepository:
    def __init__(self, session):
        self.session = session

    def add(self, review):
        self.session.add(review)
        self.session.commit()

    def get(self, id):
        return self.session.query(Review).get(id)

    def get_all(self):
        return self.session.query(Review).all()

    def update(self, id, data):
        review = self.get(id)
        if review:
            for key, value in data.items():
                setattr(review, key, value)
            self.session.commit()
        return review

    def delete(self, id):
        review = self.get(id)
        if review:
            self.session.delete(review)
            self.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.session.query(Review).filter(getattr(Review, attr_name) == attr_value).first()


class AmenityRepository:
    def __init__(self, session):
        self.session = session

    def add(self, amenity):
        self.session.add(amenity)
        self.session.commit()

    def get(self, id):
        return self.session.query(Amenity).get(id)

    def get_all(self):
        return self.session.query(Amenity).all()

    def update(self, id, data):
        amenity = self.get(id)
        if amenity:
            for key, value in data.items():
                setattr(amenity, key, value)
            self.session.commit()
        return amenity

    def delete(self, id):
        amenity = self.get(id)
        if amenity:
            self.session.delete(amenity)
            self.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.session.query(Amenity).filter(getattr(Amenity, attr_name) == attr_value).first()