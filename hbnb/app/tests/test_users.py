import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_duplicate_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

# class TestPlacesEndpoints(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app()
#         self.client = self.app.test_client()

#     def test_create_place(self):
#         owner = self.client.post('/api/v1/users/', json={
#             "first_name": "Jane",
#             "last_name": "Doe",
#             "email": "jane.doe@example.com" 
#         })
#         print(owner)
#         response = self.client.post('/api/v1/places/', json={
#             "title": "Cozy Apartment",
#             "description": "A nice place to stay",
#             "price": 100.0,
#             "latitude": 37.7749,
#             "longitude": -122.4194,
#             "owner_id": owner.id
#         })
#         self.assertEqual(response.status_code, 201)


# python3 -m unittest app/tests/test_users.py