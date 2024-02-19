from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

class LoginUserTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        register_data = {
            "name": "John Doe",
            "email": "johndoe@abc.com",
            "dob": "2000-01-01",
            "password1": "johndoe123",
            "password2": "johndoe123",
        }
        client = APIClient()
        client.post(reverse("user"), register_data, format="json")
        cls.input_data = {
            "email": register_data["email"],
            "password": register_data["password1"]
        }
    
    def setUp(self):
        self.maxDiff = None
    
    def test_valid_login(self):
        resp = self.client.post(reverse("login"), self.input_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_invalid_email(self):
        self.input_data["email"] = "ababac"
        resp = self.client.post(reverse("login"), self.input_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        exp_resp = {'errors': {'error': 'Invalid Input', 'field_errors': {'email': ['Enter a valid email address.']}}}
        self.assertEqual(exp_resp, resp.data)
    
    def test_invalid_login(self):
        self.input_data["password"] = "ababac"
        resp = self.client.post(reverse("login"), self.input_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        exp_resp = {'errors': {'error': 'Invalid Login Details'}}
        self.assertEqual(exp_resp, resp.data)
    
    