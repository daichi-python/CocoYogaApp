from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email", "sex"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
        
    def clean_username(self):
        username = self.cleaned_data["username"]
        if 6 <= len(username) <= 25: 
            return Utils.word_check("username", username)
        else:
            raise ValidationError("username length must be 6 to 25.")

    def clean_password2(self):
        super().clean_password2()
        password = self.cleaned_data["password2"]
        if 8 <= len(password) <= 30: 
            return Utils.word_check("password", password)
        else:
            raise ValidationError("password length must be 8 to 30.")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Utils.check_email_format(email) and (15 <= len(email) <= 40):
            return Utils.word_check("email", email)
        else:
            raise ValidationError("this email format is unusable")


class Utils(object):
    
    @staticmethod
    def word_check(form_name, string):
        usable_table = {
            "username": "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._-",
            "password": "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._-()",
            "email": "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._-@",
        }
        usable_words = usable_table[form_name]
        for word in string:
            if word not in usable_words:
                raise ValidationError(f"You can't use {word} in {form_name} field")
        return string

    def check_email_format(email):
        atmark = email.find("@")
        if atmark == -1:
            return False
        if email[atmark+1:].find("@") == -1 and email[atmark:].find(".") != -1:
            return True
        return False