from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, DetailView, ListView, View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.utils.timezone import make_aware
from .models import Instructer, Lesson, PoseCollection, Purchase, Question, QuestionAndAnswer, LessonStyle, Pose
from .forms import QuestionAndAnswerForm, RegisterLessonForm

import datetime
import requests
import json
import stripe

# Create your views here.
class HomeView(LoginRequiredMixin, ListView):
    template_name = "yogapp/home.html"
    model = Lesson

    def get_queryset(self):
        return Lesson.objects.order_by("lesson_date").filter(lesson_date__gte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "lesson": HomeView.get_next_lesson(Purchase.objects.filter(user=self.request.user)),
        })
        return context

    @staticmethod
    def get_next_lesson(queryset):
        """
        this funtioin use in HomeView class.
        """
        lessons = []
        for purchase in queryset:
            if purchase.lesson.lesson_date + datetime.timedelta(hours=1) >= timezone.now():
                lessons.append(purchase.lesson)

        next_lesson = None
        for lesson in lessons:
            if next_lesson is None or next_lesson.lesson_date > lesson.lesson_date:
                next_lesson = lesson
        return next_lesson


class PurchaseLessonView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "yogapp/pur_lesson.html"
    model = Lesson
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        token = request.POST["stripeToken"]
        try:
            charge = stripe.Charge.create(
                amount=lesson.price,
                currency="jpy",
                source=token,
                description="username:{} lesson date:{}".format(request.user.username, lesson.lesson_date)
            )
        except stripe.error.CardError as e:
            context = self.get_context_data()
            context["message"] = "エラーが発生しました。支払処理が完了していません。"
            return render(request, "yogapp/pur_lesson.html", context)
        else:
            Purchase.objects.create(user=request.user, lesson=lesson, stripe_id=charge.id)
            return redirect("home")
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["public_key"] = settings.STRIPE_PUBLIC_KEY
        return context
    
    def test_func(self):
        lesson = self.get_object()
        return not self.request.user.does_user_have_lesson(lesson)


class MypageView(LoginRequiredMixin, ListView):
    template_name = "yogapp/mypage.html"
    model = Purchase

    def get_queryset(self):
        return MypageView.get_future_or_past_lessons(Purchase.objects.filter(user=self.request.user), "past")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "future_lessons": MypageView.get_future_or_past_lessons(Purchase.objects.filter(user=self.request.user), "future"),
        })
        return context
    
    @staticmethod
    def get_future_or_past_lessons(purchases, time="past"):
        lessons = []

        if time == "future":
            for purchase in purchases:
                if purchase.lesson.lesson_date > timezone.now():
                    lessons.append(purchase.lesson)

        elif time == "past":
            for purchase in purchases:
                if purchase.lesson.lesson_date < timezone.now():
                    lessons.append(purchase.lesson)

        return lessons


class RegisterLessonView(LoginRequiredMixin, FormView):
    template_name = "yogapp/reg_lesson.html"
    model = LessonStyle
    form_class = RegisterLessonForm
    success_url = "yogapp/reg_lesson.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "poses": Pose.objects.all(),
        })
        return context

    def form_valid(self, form):
        if not self.request.user.is_instructer():
            return redirect("home")

        lesson_date = make_aware(datetime.datetime.strptime(form["lesson_date"].value(), "%Y-%m-%dT%H:%M"))

        if form.is_valid():
            pose_collection = RegisterLessonView.create_pose_collection(form["poses"].value())
            Lesson.objects.create(
                instructer = Instructer.objects.get(user=self.request.user),
                style = LessonStyle.objects.get(rank=form["style"].value()),
                lesson_date = lesson_date,
                whereby = RegisterLessonView.create_lesson(lesson_date),
                poses=pose_collection,
                price=int(form["price"].value()),
            )
        return redirect("instructer")

    @staticmethod
    def create_lesson(lesson_date):
        API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmFwcGVhci5pbiIsImF1ZCI6Imh0dHBzOi8vYXBpLmFwcGVhci5pbi92MSIsImV4cCI6OTAwNzE5OTI1NDc0MDk5MSwiaWF0IjoxNjM1ODU2NjI4LCJvcmdhbml6YXRpb25JZCI6MTM4NDY0LCJqdGkiOiJmY2QyM2Y1OS1hNTM2LTQ3MDItODMxMy04ZWY5NGRjZjgzMzgifQ.o-oersIo3LxpH27jIIvXZ38pGCklihPuwgkfDKkt0vk"
        URL = "https://api.whereby.dev/v1/meetings"

        data = {
            "endDate": datetime.datetime.strftime(lesson_date, "%Y-%m-%dT%H:%M:%S"),
            "fields": ["hostRoomUrl"],
            "roomMode": "group",
            "roomNamePrefix": "CocoYoga",
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            url=URL,
            headers=headers,
            json=data,
        )

        data = json.loads(response.text)
        return data["roomUrl"]
    
    @staticmethod
    def create_pose_collection(pose_ids):
        pose_collection = PoseCollection.objects.create()
        for pose_id in pose_ids:
            pose_collection.poses.add(Pose.objects.get(id=pose_id))
        return pose_collection


class QandAView(LoginRequiredMixin, FormView, ListView):
    template_name = "yogapp/Q&A.html"
    form_class = QuestionAndAnswerForm
    model = QuestionAndAnswer
    success_url = "yogapp/Q&A.html"
    
    def form_valid(self, form):
        Question.objects.create(
            user = self.request.user,
            category=form["category"].value(),
            detail=form["detail"].value(),
        )
        return redirect("qanda")


class InstructerView(LoginRequiredMixin, ListView):
    template_name = "yogapp/instructer.html"
    model = Lesson

    def get_queryset(self):
        return Lesson.objects.filter(instructer=Instructer.objects.get(user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_date = make_aware(datetime.datetime(timezone.now().year, timezone.now().month, 1))

        context.update({
            "past_lesson": self.object_list.filter(lesson_date__lte=timezone.now()).order_by("lesson_date"),
            "future_lesson": self.object_list.filter(lesson_date__gte=timezone.now()).order_by("lesson_date"),
            "this_month_lesson": self.object_list.filter(lesson_date__range=(start_date, timezone.now())),

            # get number of participants in past lesson. this context is Integer.
            "total_count": InstructerView.get_lesson_participants(self.object_list.filter(lesson_date__lte=timezone.now())),
            # get number of participants in this month lesson. this context is Integer.
            "this_month_count": InstructerView.get_lesson_participants(self.object_list.filter(lesson_date__range=(start_date, timezone.now())))
        })
        return context

    @staticmethod
    def get_lesson_participants(lessons):
        lesson_participants = 0

        for lesson in lessons:
            lesson_participants += lesson.get_number_of_participants()

        return lesson_participants


class LessonView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "yogapp/lesson.html"
    model = Lesson
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "poses": self.get_object().poses.poses.all()
        })
        return context
    
    def test_func(self):
        return self.request.user.does_user_have_lesson(self.get_object()) or self.request.user.is_instructer()
    