from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')


# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review', min_length=1),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)', min=1, max=5),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        try:
            review_data = api.payload
            review_data['author_id'] = current_user['id']
            new_review = facade.create_review(review_data)
            return {
                **new_review,
                'author': facade.get_user(new_review['author_id'])
            }, 201
        except Exception as e:
            return {'error': f"{e}"}, 400

    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return review, 200
        except Exception as e:
            return {'error': f'{e}'}, 404

    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        current_user = get_jwt_identity()
        try:
            review = facade.get_review(review_id)

            if (current_user['id'] != review['author_id']):
                return {'error': 'Unauthorized action'}, 403 

            review_data = api.payload
            review_data['author_id'] = current_user['id']
            review = facade.update_review(review_id, review_data)
            return review, 200

        except Exception as e:
            return {'error': f"{e}"}, 400

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        try:
            review = facade.get_review(review_id)

            if (current_user['id'] != review['author_id']):
                return {'error': 'Unauthorized action'}, 403 

            review_id = facade.delete_review(review_id)
            return "Review deleted successfully", 200
        except Exception as e:
            return {'error': f'{e}'}, 404
