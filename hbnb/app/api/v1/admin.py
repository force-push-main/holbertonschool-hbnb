from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('admin', description='Admin operations')

update_user = api.model('UpdateUser', {
    'email': fields.String(Required=True, description='The email of the user to update')
})

@api.route('/user')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = api.payload

        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        if 'email' not in data:
            return {'error': 'User email is required'}, 403
        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400
        
        user = facade.create_user(data)

        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }, 201

@api.route('/user/<user_id>')
class AdminUserResource(Resource):
    @api.expect(update_user)
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        data = api.payload
        
        if not current_user['is_admin']:
            return {'error': 'Admin privileges required'}, 403
        if 'email' not in data:
            return {'error': 'User email is required'}, 403
        
        email = data['email']
        
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        updated_user = facade.update_user(user_id, data)

        return {
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'is_admin': updated_user.is_admin,
        }

@api.route('/amenity')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = api.payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        if 'name' not in data:
            return {'error': '"name" is required'}, 403
        
        amenity = facade.create_amenity(data)

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 201
    
@api.route('/amenity/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        data = api.payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        if 'name' not in data:
            return {'error': '"name" is required'}, 403
        
        amenity = facade.update_amenity(amenity_id, data)

        return {
            'id': amenity.id,
            'name': amenity.name
        }