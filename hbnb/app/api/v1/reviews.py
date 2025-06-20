from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')


# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review', min_length=1),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)', min=1, max=5),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            review_data = api.payload
            new_review = facade.create_review(review_data)
            return new_review, 201
        except Exception as e:
            import traceback
            return {"error": str(e), "traceback": traceback.format_exc()}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return review, 200
        except Exception as e:
            return {'error': f'{e}'}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        try:
            review_data = api.payload
            review = facade.update_review(review_id, review_data)
            return review, 200

        except Exception as e:
            return {'error': f"{e}"}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            review_id = facade.delete_review(review_id)
            return "Review deleted successfully", 200
        except Exception as e:
            return {'error': f'{e}'}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            return facade.get_reviews_by_place(place_id), 200
        except Exception as e:
            return {'error': f"{e}"}, 404
