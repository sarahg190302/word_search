from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from users.models import CustomUser
from search.models import Paragraph

class AddParagraphTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_data = {
            "name": "John Doe",
            "email": "johndoe@abc.com",
            "dob": "2000-01-01",
            "password1": "johndoe123",
            "password2": "johndoe123",
        }
        client = APIClient()
        client.post(reverse("user"), cls.register_data, format="json")
        cls.user = CustomUser.objects.get(email=cls.register_data["email"])
    
    def setUp(self):
        self.maxDiff = None
    
    def test_authentication_required(self):
        resp = self.client.post(reverse("paragraphs"), {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        exp_resp = {
            "detail": "Authentication credentials were not provided."
        }
        self.assertEqual(resp.data, exp_resp)
    
    def test_empty_text_invalid(self):
        self.client.force_authenticate(self.user)
        resp = self.client.post(reverse("paragraphs"), {"text": ""}, format="json")
        exp_resp = {'errors': {'error': 'Invalid Input', 'field_errors': {'text': ['This field may not be blank.']}}}
        self.assertEqual(exp_resp, resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_valid_authentication(self):
        input_data = {
            "email": self.register_data["email"],
            "password": self.register_data["password1"]
        }
        resp = self.client.post(reverse("login"), input_data, format="json")
        token = resp.data["auth_token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        resp = self.client.post(reverse("paragraphs"), {"text": ""}, format="json")
        exp_resp = {'errors': {'error': 'Invalid Input', 'field_errors': {'text': ['This field may not be blank.']}}}
        self.assertEqual(exp_resp, resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_valid_input(self):
        self.client.force_authenticate(self.user)
        with open("./search/tests/paras.txt") as f:
            text = f.read()
        resp = self.client.post(reverse("paragraphs"), {"text": text}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        para_count = Paragraph.objects.count()
        self.assertEqual(3, para_count)

    
    