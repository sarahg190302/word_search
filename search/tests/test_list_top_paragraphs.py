from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from users.models import CustomUser
from search.models import Paragraph, Word, WordParagraphMap

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
        with open("./search/tests/paras.txt") as f:
            text = f.read()
        client.force_authenticate(cls.user)
        client.post(reverse("paragraphs"), {"text": text}, format="json")
        cls.input_data = {
            "word": "the",
            "top_n": 2
        }

    
    def setUp(self):
        self.maxDiff = None
    
    def test_authentication_required(self):
        resp = self.client.get(reverse("paragraphs"), {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        exp_resp = {
            "detail": "Authentication credentials were not provided."
        }
        self.assertEqual(resp.data, exp_resp)
    
    def test_inputs_required(self):
        self.client.force_authenticate(self.user)
        self.input_data["word"] = ""
        self.input_data.pop("top_n")
        resp = self.client.get(reverse("paragraphs"), self.input_data, format="json")
        exp_resp = {'errors': {'error': 'Invalid Input', 'field_errors': {'word': ['This field may not be blank.'], "top_n": ["A valid integer is required."]}}}
        self.assertEqual(exp_resp, resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_word_not_found(self):
        self.client.force_authenticate(self.user)
        self.input_data["word"] = "sakjdhaskdjhask"
        resp = self.client.get(reverse("paragraphs"), self.input_data, format="json")
        exp_resp = {"errors": {"error": "Word Not Found"}}
        self.assertEqual(exp_resp, resp.data)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_valid_input(self):
        self.client.force_authenticate(self.user)   
        resp = self.client.get(reverse("paragraphs"), self.input_data, format="json")
        with open("./search/tests/paras.txt") as f:
            text = f.read()
        paras = text.strip().split("\n\n")
        exp_resp = [paras[0], paras[2]]
        self.assertEqual(exp_resp, resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)



    
    
    
    