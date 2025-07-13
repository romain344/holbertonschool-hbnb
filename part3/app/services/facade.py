from app.models.user import User
from app.models.amenty import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository()
        self.place_repository = SQLAlchemyRepository()
        self.review_repository = SQLAlchemyRepository()
        self.amenity_repository = SQLAlchemyRepository()

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
        user = self.user_repository.get(user_id)
        if not user:
            return None
        self.user_repository.update(user_id, user_data)
        return user

    # ------------------ AMENITIES ------------------ #

    def create_amenity(self, amenity_data):
        new_amenity = Amenity(**amenity_data)
        self.amenity_repository.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repository.get(amenity_id)
        if not amenity:
            return False
        self.amenity_repository.update(amenity_id, amenity_data)
        return True

    # ------------------ PLACES ------------------ #

    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id', None)
        if not owner_id:
            raise ValueError("owner_id is required")

        owner = self.user_repository.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        amenities_ids = place_data.pop('amenities', [])
        place_data['owner'] = owner
        place = Place(**place_data)

        for amenity_id in amenities_ids:
            amenity = self.amenity_repository.get(amenity_id)
            if amenity:
                place.amenities.append(amenity)

        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repository.get(place_id)
        if not place:
            return None
        self.place_repository.update(place_id, place_data)
        return place

    # ------------------ REVIEWS ------------------ #

    def create_review(self, review_data):
        user = self.user_repository.get(review_data.get("user_id"))
        place = self.place_repository.get(review_data.get("place_id"))

        if not user or not place:
            raise ValueError("User or Place not found")

        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user=user,
            place=place
        )
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        return [
            r for r in self.review_repository.get_all() if r.place.id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = self.review_repository.get(review_id)
        if not review:
            return None
        self.review_repository.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repository.get(review_id)
        if not review:
            return False
        self.review_repository.delete(review_id)
        return True