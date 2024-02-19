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
        input_data = {
            "email": register_data["email"],
            "password": register_data["password1"]
        }
        resp = client.post(reverse("login"), input_data, format="json")
        cls.token = resp.data["auth_token"]
    
    def setUp(self):
        self.maxDiff = None
    
    def test_valid_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        resp = self.client.post(reverse("logout"), {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_invalid_logout(self):
        resp = self.client.post(reverse("logout"), {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(resp.data, {"detail": "Authentication credentials were not provided."})
    
    