from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
import re


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    """User"""
    def create_user(self, user_data):
        if not user_data['first_name']:
            raise ValueError("First name cannot be blank")
        if not user_data['last_name']:
            raise ValueError("Last name cannot be blank")
        if not user_data['email']:
            raise ValueError("Email cannot be blank")
        if not re.fullmatch(r"^[a-zA-Z0-9_.±]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$", user_data['email']):
            raise ValueError("Email must be valid")
        if self.get_user_by_email(user_data['email']):
            raise ValueError("Email already registered")
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def delete_user(self, user_id):
        self.user_repo.delete(user_id)

    """Amenity"""
    def check_amenity_exists(self, amenity_name):
        amenities = self.amenity_repo.get_all()
        clean_name = re.sub(r'[^a-z]', '', amenity_name.lower())
        existing_amenity = next((amenity for amenity in amenities if 
                 re.sub(r'[^a-z]', '', getattr(amenity, 'name', '').lower()) == clean_name), None)
        return existing_amenity

    def create_amenity(self, amenity_data):
        if not amenity_data['name']:
            raise ValueError("Amenity name cannot be blank")

        if self.check_amenity_exists(amenity_data['name']):
            raise ValueError("Amenity already exists")

        amenity_data['name'] = amenity_data['name'].title()

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        json_data = []
        for instance in amenities:
            response = {
                "id": instance.id,
                "name": instance.name
            }
            json_data.append(response)

        return json_data

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    """Place"""
    def create_place(self, place_data):

        #check format + up to 100 characters length
        if (type (place_data['title']) != str or
                len(place_data['title']) == 0 or
                len(place_data['title']) > 100):
            raise ValueError("Place must have a title")

        if not place_data['description']:
            raise ValueError("Place must have a description")

        #check price format and value
        if (type(place_data['price']) != float or 
                place_data['price'] < 0.0):
            raise ValueError("Place must have a price")

        #check latitude format + value
        if (type (place_data['latitude']) != float or
                place_data['latitude'] < -90.0 or
                place_data['latitude'] > 90.0):
            raise ValueError("Place must have a latitude")

        #check longitude format + value
        if (type (place_data['longitude']) != float or
                place_data['longitude'] < -180.0 or
                place_data['longitude'] > 180.0):
            raise ValueError("Place must have a longitude")

        if not place_data['owner_id']:
            raise ValueError("Place must have an owner")

        owner = self.user_repo.get_by_attribute('id', place_data["owner_id"])
        if not owner:
            raise ValueError("Place must have a valid owner")

        place_obj = dict(place_data)
        place_obj.pop('owner_id')
        place_obj.pop('amenities')

        place_obj['owner'] = owner
        amenities_list = []

        for amenity_name in place_data["amenities"]:
            existing_amenity = self.check_amenity_exists(amenity_name)
            if not existing_amenity:
                existing_amenity = self.create_amenity({"name": amenity_name})
            amenities_list.append(existing_amenity)
        place_obj['amenities'] = amenities_list

        place = Place(**place_obj)
        self.place_repo.add(place)

        new_place_dict = {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "user_id": place.owner.id,
            "amenities": [amenity.name for amenity in place.amenities]
        }
        return new_place_dict

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner.id,
            "amenities": [amenity.name for amenity in place.amenities]
            }

    def get_all_places(self):
        places = self.place_repo.get_all()
        places_list = []
        for place in places:
            place_obj = {
                "id": place.id,
                "title": place.title,
                "latitude": place.latitude,
                "longitude": place.longitude,
            }
            places_list.append(place_obj)
        return places_list

    def update_place(self, place_id, place_data):

        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError("Place not found")

        #check format + up to 100 characters length
        if 'title' in place_data:
            if (type (place_data['title']) != str or
                    len(place_data['title']) == 0 or
                    len(place_data['title']) > 100):
                raise ValueError("Place must have a title")

        # check format for description
        if 'description' in place_data:
            if type(place_data['description']) != str:
                raise ValueError("Place must have a description")

        #check price format and value
        if 'price' in place_data:
            if (type (place_data['price']) != float or 
                    place_data['price'] < 0.0):
                raise ValueError("Place must have a price")

        #check latitude format + value
        if 'latitude' in place_data:
            if (type (place_data['latitude']) != float or
                    place_data['latitude'] < -90.0 or
                    place_data['latitude'] > 90.0):
                raise ValueError("Place must have a latitude")

        #check longitude format + value
        if 'longitude' in place_data:
            if (type (place_data['longitude']) != float or
                    place_data['longitude'] < -180.0 or
                    place_data['longitude'] > 180.0):
                raise ValueError("Place must have a longitude")

        place_obj = dict(place_data)
        """no matter outcome of next checks, place_obj shouldn't have a field for owner_id or amenities 
        because Place takes class objects, not strings for these fields, and pop safely removes key-values 
        without throwing errors if the key doesn't exist"""
        place_obj.pop('owner_id')
        place_obj.pop('amenities')

        if 'owner_id' in place_data:
            if not place_data['owner_id']:
                raise ValueError("Place must have an owner")
            new_owner = self.user_repo.get(place_data["owner_id"])
            if not new_owner:
                raise ValueError("Place must have a valid owner")
            curr_owner_id = place.owner.id
            if new_owner.id != curr_owner_id:
                place_obj['owner'] = new_owner

        if 'amenities' in place_data:
            amenities_list = []
            for amenity_name in place_data["amenities"]:
                existing_amenity = self.check_amenity_exists(amenity_name)
                if not existing_amenity:
                    existing_amenity = self.create_amenity({"name": amenity_name})
                amenities_list.append(existing_amenity)
            place_obj['amenities'] = amenities_list

        self.place_repo.update(place_id, place_obj)
        updated_place = self.place_repo.get(place_id)
        new_place_dict = {
            "title": updated_place.title,
            "description": updated_place.description,
            "price": updated_place.price,
            "latitude": updated_place.latitude,
            "longitude": updated_place.longitude
            # "owner_id": updated_place.owner.id
            # "amenities": [amenity.name for amenity in updated_place.amenities]
        }
        return new_place_dict

    """Review"""

    def create_review(self, review_data):
        if not review_data['text']:
            raise ValueError("Review must contain text")
        if not review_data['rating']:
            raise ValueError("Review must contain rating")
        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])
        if not user:
            raise ValueError("Review must be from a valid user")
        if not place:
            raise ValueError("Review must be for a valid place")
        review_obj = {
            "text": review_data['text'],
            "rating": review_data['rating'],
            "author": user,
            "place": place
        }
        review = Review(**review_obj)
        self.review_repo.add(review)
        new_review_dict = {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.author.id,
            "place_id": review.place.id
        }
        return new_review_dict

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        new_review_dict = {
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }
        return new_review_dict

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        reviews_list = []
        for review in reviews:
            review_object = {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
            }
            reviews_list.append(review_object)
        return reviews_list

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        print('hello world')
        if not place:
            raise ValueError("Place not found")
        reviews = []
        for review in place.reviews:
            review_object = {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
            }
            reviews.append(review_object)
        return reviews

    def update_review(self, review_id, review_data):
        if not self.review_repo.get(review_id):
            raise ValueError("Review does not exist")
        if 'text' in review_data:
            if not review_data['text']:
                raise ValueError("Review must contain text")
        if 'rating' in review_data:
            if not review_data['rating']:
                raise ValueError("Review must contain rating")
        self.review_repo.update(review_id, review_data)
        new_review = self.review_repo.get(review_id)
        new_review_dict = {
            "text": new_review.text,
            "rating": new_review.rating
        }
        return new_review_dict

    def delete_review(self, review_id):
        if not self.review_repo.get(review_id):
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)