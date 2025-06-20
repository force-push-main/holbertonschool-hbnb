import unittest
from app import create_app
import json

class TestReviewsEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        test_user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        create_new_user = self.client.post('/api/v1/users/', json=test_user_data)

        user = json.loads(create_new_user.get_data(as_text=True))
        test_place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user['id'],
            "amenities": ['pool', 'Wi-fi']
            }
        create_new_place = self.client.post('/api/v1/places/', json=test_place_data)
        place = json.loads(create_new_place.get_data(as_text=True))

        new_review = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user['id'],
            "place_id": place['id']
        }
        response = self.client.post('/api/v1/reviews/', json=new_review)
        self.assertEqual(response.status_code, 201)