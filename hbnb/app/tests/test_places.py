import unittest
from app import create_app
import json

class TestPlacesEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.test_user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        self.test_place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": None,
            "amenities": ['pool', 'Wi-fi']
            }

    def test_create_place(self):
        create_new_user = self.client.post('/api/v1/users/', json=self.test_user_data)
        new_user = json.loads(create_new_user.get_data(as_text=True))
        self.test_place_data['owner_id'] = new_user['id']
        response = self.client.post('/api/v1/places/', json=self.test_place_data)
        returned_data = json.loads(response.get_data(as_text=True))
        self.test_place_data = returned_data
        self.assertEqual(response.status_code, 201)

    def test_create_place_error(self):
        test_place_data = {
            "title": "",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.test_place_data['owner_id'],
            "amenities": ['pool', 'Wi-Fi']
            }
        response = self.client.post('/api/v1/places/', json=test_place_data)
        self.assertEqual(response.status_code, 400)

    # def test_update_place(self):
    #     updated_data = {
    #         "title": "new title"
    #     }
    #     print(self.test_place_data['id'])
        # url = "/api/v1/places/" + self.test_place_data['id']
        # response = self.client.post(url, json=updated_data)
        # returned_data = json.loads(response.get_data(as_text=True)) 
        # print(returned_data)
        # self.assertEqual(response.status_code, 201)

