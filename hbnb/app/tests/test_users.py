import unittest
from app import create_app
import json

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.test_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }

    def create_user(self):
        return self.client.post('/api/v1/users/', json=self.test_data)

    def test_create_user(self):
        response = self.create_user()
        self.assertEqual(response.status_code, 201)

    def test_duplicate_user(self):
        response = self.client.post('/api/v1/users/', json=self.test_data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
