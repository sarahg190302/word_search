from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import CustomUser
from rest_framework import status

class RegisterUserTestCase(APITestCase):
    def setUp(self):
        self.input_data = {
            "name": "John Doe",
            "email": "johndoe@abc.com",
            "dob": "2000-01-01",
            "password1": "johndoe123",
            "password2": "johndoe123",
        }
        self.maxDiff = None
    
    def test_valid_registration(self):
        self.assertEqual(0, CustomUser.objects.count())
        resp = self.client.post(reverse("user"), self.input_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, CustomUser.objects.count())

    def test_invalid_email(self):
        self.input_data["email"] = "ababac"
        resp = self.client.post(reverse("user"), self.input_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        exp_resp = {'errors': {'error': 'Invalid Input', 'field_errors': {'email': ['Enter a valid email address.']}}}
        self.assertEqual(exp_resp, resp.data)
    
    def test_invalid_dob(self):
        self.input_data["dob"] = "2000011"
        resp = self.client.post(reverse("user"), self.input_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        exp_resp = {'errors': {'error': 'Invalid Input', 'field_errors': {'dob': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']}}}
        self.assertEqual(exp_resp, resp.data)
    
    def test_passwords_dont_match(self):
        self.input_data["password2"] = "johndoe12"
        resp = self.client.post(reverse("user"), self.input_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        exp_resp = {'errors': {'error': 'Invalid Input', 'field_errors': {'non_field_errors': ['Passwords dont match']}}}
        self.assertEqual(exp_resp, resp.data)
    
    def test_email_already_exists(self):
        resp = self.client.post(reverse("user"), self.input_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.client.post(reverse("user"), self.input_data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
        exp_resp = {'errors': {'error': 'Email Already Exists'}}
        self.assertEqual(exp_resp, resp.data)