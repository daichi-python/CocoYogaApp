from django.urls import path
from .views import LandingpageView, Login, LogoutView, Register, RegisterComplete, RegisterDone

urlpatterns = [
    path("landing/", LandingpageView.as_view(), name="landing"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", Register.as_view(), name="user_register"),
    path("register/done/", RegisterDone.as_view(), name="register_done"),
    path("register/complete/<token>/", RegisterComplete.as_view(), name="register_complete"),
]