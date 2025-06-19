from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
import re


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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
    def create_amenity(self, amenity_data):
        if not amenity_data['name']:
            raise ValueError("Amenity name cannot be blank")

        clean_name = re.sub(r'[^a-z]', '', amenity_data['name'].lower())
        if next((amenity for amenity in self.amenity_repo._storage.values() if 
                 re.sub(r'[^a-z]', '', getattr(amenity, 'name', '').lower()) == clean_name), None):
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
        if (type (place_data['price']) != float or 
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
            clean_name = re.sub(r'[^a-z]', '', amenity_name.lower())
            existing_amenity = next((amenity for amenity in self.amenity_repo._storage.values() if 
            re.sub(r'[^a-z]', '', getattr(amenity, 'name', '').lower()) == clean_name), None)
            if not existing_amenity:
                existing_amenity = self.create_amenity({"name": amenity_name})
            amenities_list.append(existing_amenity)
        place_obj['amenities'] = amenities_list

        place = Place(**place_obj)
        self.place_repo.add(place)

        new_place_dict = {
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner.id,
            "amenities": [amenity.name for amenity in place.amenities]
        }
        return new_place_dict

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):

        place = self.place_repo.get_by_attribute('id', place_data['place_id'])
        if not place:
            return {"error": "Place not found"}, 404

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

        """need to add check on whether owner has changed, and if so 
        then go through same process as above of adding an owner instance to the place object
        rather than just the owner id"""

        place_obj = dict(place_data)


        # if 'owner_id' in place_data:
        #     if not place_data['owner_id']:
        #         raise ValueError("Place must have an owner")
        #     owner = self.user_repo.get_by_attribute('id', place_data["owner_id"])
        #     if not owner:
        #         raise ValueError("Place must have a valid owner")
        #     
        #     if place_data['owner_id'] == owner.id:
        #         place_obj.pop('owner_id')
        #     else:
        #         place_obj['owner'] = owner

        """Also need to check whether the amenities have changed, and if so
        then go through same process as above of checking if amenities already exist, and
        either adding existing amenities objects to dict, or else creating new amenities objects
        and adding to dict
        should be easy enough :')"""

        # if 'amenities' in place_data:
        #     place_obj.pop('amenities')

        # amenities_list = []

        # for amenity_name in place_data["amenities"]:
        #     clean_name = re.sub(r'[^a-z]', '', amenity_name.lower())
        #     existing_amenity = next((amenity for amenity in self.amenity_repo._storage.values() if 
        #     re.sub(r'[^a-z]', '', getattr(amenity, 'name', '').lower()) == clean_name), None)
        #     if not existing_amenity:
        #         existing_amenity = self.create_amenity({"name": amenity_name})
        #     amenities_list.append(existing_amenity)
        # place_obj['amenities'] = amenities_list

        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)


    """Review"""
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
        return review_id