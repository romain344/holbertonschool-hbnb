from app.persistence.repository import InMemoryRepository
from app.models import User, Amenity
from app.models import Review, Place
from app.models.user import User



class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users from the database"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        self.user_repo.update(user_id, user)
        return user

    def create_amenity(self, amenity_data):
        new_amenity = Amenity(**amenity_data)
        self.amenity_repo.add(new_amenity)
        return new_amenity.to_dict()

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            return amenity.to_dict()
        return None

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        self.amenity_repo.update(amenity_id, amenity)
        return True

    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id', None)
        if not owner_id:
            raise ValueError("owner_id is required")
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        amenities_ids = place_data.pop('amenities', [])
        place_data['owner'] = owner
        place = Place(**place_data)
        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.amenities.append(amenity)
        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            return place.to_dict()
        return None

    def get_all_places(self):
        return [place.to_dict() for place in self.place_repo.get_all()]
        
    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for key, value in place_data.items():
            setattr(place, key, value)
        self.place_repo.update(place_id, place_data)
        return place.to_dict()

    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get("user_id"))
        place = self.place_repo.get(review_data.get("place_id"))

        if not user or not place:
            raise ValueError("User or Place not found")

        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user=user,
            place=place
        )
        self.review_repo.add(review)  # Correction ici
        return review.to_dict() 

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            return review.to_dict()
        return None

    def get_all_reviews(self):
        return [r.to_dict() for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        return [r.to_dict() for r in reviews if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']

        self.review_repo.update(review_id, review)
        return review.to_dict()

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True