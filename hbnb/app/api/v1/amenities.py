from flask_restx import Namespace, Resource, fields
from app.services import facade
import re

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    def post(self):
        """Register a new amenity"""
        try:
            amenity_data = api.payload

            new_amenity = facade.create_amenity(amenity_data)
            return {
                "id": new_amenity.id,
                "name": new_amenity.name
            }, 201
        except Exception as e:
            return {"Error": f'{e}'}, 400
    
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return amenities

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 400
        return {
            'id': amenity.id,
            "name": amenity.name
        }, 200

    @api.expect(amenity_model)
    def put(self, amenity_id):
        try:
            """Update an amenity's information"""
            amenity_data = api.payload
        
            #check the amenity exists
            amenity = facade.update_amenity(amenity_id, amenity_data)
            if not amenity:
                return {"error": "Amenity not found"}, 404
            return {
                "id": amenity.id,
                "name": amenity.name
            }, 200
        except Exception as e:
            return {"error": f"{e}"}, 400
