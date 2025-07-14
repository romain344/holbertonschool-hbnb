from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    # ------------------ USERS ------------------ #

    def create_user(self, user_data):
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password']
        )
        self.user_repository.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repository.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repository.update(user_id, user_data)

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)

    # ------------------ AMENITIES ------------------ #

    def create_amenity(self, amenity_data):
        new_amenity = Amenity(name=amenity_data["name"])
        self.amenity_repository.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repository.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        return self.amenity_repository.delete(amenity_id)

    # ------------------ PLACES ------------------ #

    def create_place(self, place_data):
        place = Place(
            title=place_data["title"],
            description=place_data["description"],
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"]
        )
        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repository.update(place_id, place_data)

    def delete_place(self, place_id):
        return self.place_repository.delete(place_id)

    # ------------------ REVIEWS ------------------ #

    def create_review(self, review_data):
        review = Review(
            text=review_data["text"],
            rating=review_data["rating"]
        )
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def update_review(self, review_id, review_data):
        return self.review_repository.update(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)