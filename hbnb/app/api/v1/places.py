#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        #check format + up to 100 characters length
        if (type (place_data['title']) != str or
                len(place_data['title']) == 0 or
                len(place_data['title']) > 100):
            return {"error": "Invalid input data"}, 400
        
        #check price format and value
        if (type (place_data['price']) != float or 
                place_data['price'] < 0.0):
            return {"error": "Invalid input data"}, 400
        
        #check latitude format + value
        if (type (place_data['latitude']) != float or
                place_data['latitude'] < -90.0 or
                place_data['latitude'] > 90.0):
            return {"error": "Invalid input data"}, 400
        
        #check longitude format + value
        if (type (place_data['longitude']) != float or
                place_data['longitude'] < -180.0 or
                place_data['longitude'] > 180.0):
            return {"error": "Invalid input data"}, 400
        
        new_place = facade.create_place(place_data)
        return {
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": new_place.owner_id,
            "amenities": new_place.amenities
        }

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return {
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "amenities": place.amenities
        }

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        place_data = api.payload

        #check format + up to 100 characters length
        if (type (place_data['title']) != str or
                len(place_data['title']) == 0 or
                len(place_data['title']) > 100):
            return {"error": "Invalid input data"}, 400
        
        #check price format and value
        if (type (place_data['price']) != float or 
                place_data['price'] < 0.0):
            return {"error": "Invalid input data"}, 400
        
        #check latitude format + value
        if (type (place_data['latitude']) != float or
                place_data['latitude'] < -90.0 or
                place_data['latitude'] > 90.0):
            return {"error": "Invalid input data"}, 400
        
        #check longitude format + value
        if (type (place_data['longitude']) != float or
                place_data['longitude'] < -180.0 or
                place_data['longitude'] > 180.0):
            return {"error": "Invalid input data"}, 400
        
        """Update a place's information"""
        place = facade.update_place(place_id, place_data)
        if not place:
            return {"error": "Place not found"}
        return {
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "amenities": place.amenities
        }

        

        