from django.urls import path

from .views import AnswerView, QuestionListView, HomeView, LessonView, MypageView, PoseView, PurchaseLessonView, QandAView, RegisterLessonView, InstructerView

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("purchase/<int:pk>/", PurchaseLessonView.as_view(), name="purchase"),
    path("mypage/", MypageView.as_view(), name="mypage"),
    path("register/", RegisterLessonView.as_view(), name="register"),
    path("qanda/", QandAView.as_view(), name="qanda"),
    path("instructer/", InstructerView.as_view(), name="instructer"),
    path("lesson/<int:pk>", LessonView.as_view(), name="lesson"),
    path("questionlist/", QuestionListView.as_view(), name="question_list"),
    path("pose/", PoseView.as_view(), name="pose"),
    path("answer/<int:pk>/", AnswerView.as_view(), name="answer")
]
