from django.test import TestCase
from django.contrib.auth import get_user_model
from registration.forms import LoginForm, RegisterForm
from registration.models import User

import datetime


# Create your tests here.
class LoginFormTest(TestCase):

    def setUp(self):
        User.objects.create_user(username="test_user", password="test0630", email="test@gmail.com")

    # Return False if an attempt is made to log in as a non-registerd user.
    def test_nothing_user_login(self):
        form_data = {
            "username": "error_user",
            "password": "error_pass_1234"
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    # Return False if the password is wrong.
    def test_wrong_password_login(self):
        form_data = {
            "username": "test_user",
            "password": "error_pass_1234"
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    # Returns True if the user logged in with the correct username and password.
    def test_correct_user_login(self):
        params = {
            "username": "test_user",
            "password": "test0630"
        }
        form = LoginForm(data=params)
        self.assertTrue(form.is_valid())


class RegisterFormTest(TestCase):
    
    def setUp(self):
        self.model = get_user_model()

    # Return True because only usable characters are used.
    def test_create_user_by_correct_params(self):
        params1 = {
            "username": "testuser_testuser._-20len",
            "password1": "te.st-()testpass_testpass30len",
            "password2": "te.st-()testpass_testpass30len",
            "email": "len40xxxxxxxxxxxxxxxxxxxxxxxxx@gmail.com",
            "sex": "man",
        }
        params2 = {
            "username": "len6ue",
            "password1": "te.slen8",
            "password2": "te.slen8",
            "email": "len15@gmail.com",
            "sex": "man",
        }
        form1 = RegisterForm(data=params1)
        form2 = RegisterForm(data=params2)
        self.assertTrue(form1.is_valid())
        self.assertTrue(form2.is_valid())

    # Return False because the two passwords are different
    def test_create_user_by_wrong_password(self):
        params = {
            "username": "testuser",
            "password1": "test0630",
            "password2": "test1234",
            "email": "aaabbbxxx@gmail.com",
            "sex": "man",
        }
        form = RegisterForm(data=params)
        self.assertFalse(form.is_valid())

    # Return False because the username field uses characters that cannot be used
    def test_create_user_with_using_unusable_words_in_username(self):
        params = {
            "username": "testuser!",
            "password1": "test0630",
            "password2": "test0630",
            "email": "aaabbbxxx@gmail.com",
            "sex": "man",
        }
        form = RegisterForm(data=params)
        self.assertFalse(form.is_valid())

    # Return False because the password field uses characters that cannot be used.
    def test_create_user_with_using_unusable_words_in_password(self):
        params = {
            "username": "testuser",
            "password1": "test$06&30",
            "password2": "test$06&30",
            "email": "aaabbbxxx@gmail.com",
            "sex": "man",
        }
        form = RegisterForm(data=params)
        self.assertFalse(form.is_valid())

    # Return False because the email field uses characters that cannot be used.
    def test_create_user_with_using_unusable_words_in_email(self):
        params = {
            "username": "testuser",
            "password1": "test0630",
            "password2": "test0630",
            "email": "(aaa!bbb&xxx)@gmail.com",
            "sex": "man",
        }
        form = RegisterForm(data=params)
        self.assertFalse(form.is_valid())

    # check format of email
    def test_create_user_with_unusable_email(self):
        params1 = {
            "username": "testuser",
            "password1": "test0630",
            "password2": "test0630",
            "email": "aaab@bbxxx@gmail.com",
            "sex": "man",
        }
        params2 = {
            "username": "testuser",
            "password1": "test0630",
            "password2": "test0630",
            "email": "aaabbbxxx@gmailcom",
            "sex": "man",
        }
        form1 = RegisterForm(data=params1)
        form2 = RegisterForm(data=params2)
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())
    
    def test_on_the_number_of_characters_in_username(self):
        params1 = {
            "username": "test5",
            "password1": "test0630",
            "password2": "test0630",
            "email": "aaabbbxxx@gmail.com",
            "sex": "man",
        }
        params2 = {
            "username": "testusertestusertestuser26",
            "password1": "test0630",
            "password2": "test0630",
            "email": "aaabbbxxx@gmail.com",
            "sex": "man",
        }
        form1 = RegisterForm(data=params1)
        form2 = RegisterForm(data=params2)
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())

    def test_on_the_number_of_characters_in_password(self):
        params1 = {
            "username": "testuser",
            "password1": "te_len7",
            "password2": "te_len7",
            "email": "aaabbbxxx@gmail.com",
            "sex": "man",
        }
        params2 = {
            "username": "testuser",
            "password1": "test0630test0630test0630telen31",
            "password2": "test0630test0630test0630telen31",
            "email": "aaabbbxxx@gmail.com",
            "sex": "man",
        }
        form1 = RegisterForm(data=params1)
        form2 = RegisterForm(data=params2)
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())

    def test_on_the_number_of_characters_in_email(self):
        params1 = {
            "username": "testuser",
            "password1": "test0630",
            "password2": "test0630",
            "email": "en14@gmail.com",
            "sex": "man",
        }
        params2 = {
            "username": "testuser",
            "password1": "test0630",
            "password2": "test0630",
            "email": "len41aaabbbcccdddeeefffgggxxx41@gmail.com",
            "sex": "man",
        }
        form1 = RegisterForm(data=params1)
        form2 = RegisterForm(data=params2)
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())