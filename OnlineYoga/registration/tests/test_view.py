from django.core.signing import dumps
from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from registration.models import User


class RegistrationViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.correct_params = {
            "username": "testuser",
            "password1": "test0630",
            "password2": "test0630",
            "email": "aaabbbxxx@gmail.com",
            "sex": "man",
        }
    
    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_register_view(self):
        response = self.client.get(reverse("user_register"))
        self.assertEqual(response.status_code, 200)

    def test_landing_view(self):
        response = self.client.get(reverse("landing"))
        self.assertEqual(response.status_code, 200)

    def test_register_done_view(self):
        response = self.client.get(reverse("register_done"))
        self.assertEqual(response.status_code, 200)

    # Return 200 if accessed with the correct token.
    def test_register_complete_view_by_correct_token(self):
        self.client.post(reverse("user_register"), self.correct_params)
        test_user = User.objects.get(username="testuser")
        token = dumps(test_user.pk)
        response = self.client.get(reverse("register_complete", args=(token,)))
        self.assertEqual(response.status_code, 200)

    # Return 400 if accessed with the wrong token.
    def test_register_complete_view_by_wrong_token(self):
        self.client.post(reverse("user_register"), self.correct_params)
        token = "randomwordsthisiswrongtokenthistestreturnfalse"
        response = self.client.get(reverse("register_complete", args=(token,)))
        self.assertEqual(response.status_code, 400)