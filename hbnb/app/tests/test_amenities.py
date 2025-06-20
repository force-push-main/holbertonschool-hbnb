import unittest
from app import create_app

class TestAmenitiesEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def create_(self):
        return self.client.post('/api/v1/users/', json=self.test_data)

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "Wi-fi"})
        self.assertEqual(response.status_code, 201)

    def test_duplicate_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "wifi"})
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)