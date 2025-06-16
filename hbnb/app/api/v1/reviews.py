from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
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
        review_data = api.payload

        # Check review is valid format
        if (type(review_data['text']) != str or
                len(review_data['text']) == 0):
            return {"error": "Invalid input data"}, 400
        if (type(review_data['rating']) != int or
                review_data['rating'] > 5 or
                review_data['rating'] < 1):
            return {"error": "Invalid input data"}, 400

        # Check user and place exists
        if (not facade.get_user(review_data['user_id']) or 
                not facade.get_place(review_data['place_id'])):
            return {"error": "Invalid input data"}, 400
        
        """Register a new review"""
        new_review = facade.create_review(review_data)
        return {
"text": new_review.text, "rating": new_review.rating}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 400
        return {
                "text": review['text'],
                "rating": review["rating"],
                "user_id": review["user_id"],
                "place_id": review["place_id"]
                }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        review_data = api.payload

        # Check review is valid format
        if (type(review_data['text']) != str or
                len(review_data['text']) == 0):
            return {"error": "Invalid input data"}, 400
        if (type(review_data['rating']) != int or
                review_data['rating'] > 5 or
                review_data['rating'] < 1):
            return {"error": "Invalid input data"}, 400

        # Check user and place exists
        if (not facade.get_user(review_data['user_id']) or 
                not facade.get_place(review_data['place_id'])):
            return {"error": "Invalid input data"}, 400

        """Update a review's information"""
        review = facade.update_review(review_id, review_data)
        if not review:
            return {"error": "Review not found"}
        return {
                "text": review['text'],
                "rating": review["rating"],
                "user_id": review["user_id"],
                "place_id": review["place_id"]
                }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review_id = facade.delete_review(review_id)
        if not review_id:
            return {"error": "Review not found"}, 404
        return "Review deleted successfully", 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        if not facade.get_place(place_id):
            return {"error": "Place not found"}, 404
        return facade.get_reviews_by_place(place_id)
