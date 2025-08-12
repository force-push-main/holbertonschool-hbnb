from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', min_len=1),
    'last_name': fields.String(required=True, description='Last name of the user', min_len=1),
    'email': fields.String(required=True, description='Email of the user', min_len=1),
    'password': fields.String(required=True, description='Password for the user'),
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        """Register a new user"""
        try:
            user_data = api.payload
            new_user = facade.create_user(user_data)

            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
            }, 201
        except Exception as e:
            return {'error': f'{e}'}, 400

@api.route('/<user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user['id'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email']
        }, 200

    def delete(self, user_id):
        """Delete a review"""
        try:
            facade.delete_user(user_id)
            return "User deleted successfully", 200
        except Exception as e:
            return {'error': f'{e}'}, 404

# We can remove this whenever.
# It's just a basic example on how to protect routes.
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        return {'message': f'Hello, user {current_user["id"]}'}, 200