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
    def post(self):
        """Register a new place"""
        try:
            place_data = api.payload
            place = facade.create_place(place_data)
            return place, 201
        except Exception as e:
            return {"error": f'{e}'}, 400

    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
        except Exception as e:
            return {'error': f'{e}'}, 404

    @api.expect(place_model)
    def put(self, place_id):
        """Update a place's information"""
        try:
            place_data = api.payload
            place = facade.update_place(place_id, place_data)
            return place

        except KeyError as e:
            return {'error': f'{e}'}, 404
        except Exception as e:
            return {"error": f"{e}"}, 400
