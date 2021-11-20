from django.urls import path

from .views import HomeView, LessonView, MypageView, PurchaseLessonView, QandAView, RegisterLessonView, InstructerView

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("purchase/<int:pk>/", PurchaseLessonView.as_view(), name="purchase"),
    path("mypage/", MypageView.as_view(), name="mypage"),
    path("register/", RegisterLessonView.as_view(), name="register"),
    path("qanda/", QandAView.as_view(), name="qanda"),
    path("instructer/", InstructerView.as_view(), name="instructer"),
    path("lesson/<int:pk>", LessonView.as_view(), name="lesson")
]
