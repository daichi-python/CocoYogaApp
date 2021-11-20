from django.test import TestCase
from django.urls import reverse
from yogapp.forms import QuestionAndAnswerForm, RegisterLessonForm
from yogapp.models import LessonStyle, Instructer, Lesson, Pose, PoseCollection
from registration.models import User
from django.utils import timezone

import datetime
import random

class QandAFormTest(TestCase):

    def test_send_question_form(self):
        contents = {
            "category": "1",
            "detail": "hello world. this is form test. this test returns True."
        }
        form = QuestionAndAnswerForm(data=contents)
        self.assertTrue(form.is_valid())

    def test_send_question_form_unusable_detail(self):
        contents1 = {
            "category": "1",
            "detail": "helloworld.return 0"
        }
        contents2 = {
            "category": "1",
            "detail": "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901"
        }
        form1 = QuestionAndAnswerForm(data=contents1)
        form2 = QuestionAndAnswerForm(data=contents2)
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())


class RegisterLessonFormTest(TestCase):

    def setUp(self):
        past = timezone.now() + datetime.timedelta(-1)
        future = timezone.now() + datetime.timedelta(1)
        far_future = timezone.now() + datetime.timedelta(367)
        self.past = Utils.create_datetime_string(past)
        self.future = Utils.create_datetime_string(future)
        self.far_future = Utils.create_datetime_string(far_future)
        Utils.create_pose_collection()

    # Testing for datetime
    def test_register_lesson_form(self):
        content1 = {
            "style": "normal",
            "lesson_date": self.future,
            "poses": Pose.objects.all(),
            "price": "1000"
        }
        content2 = {
            "style": "premium",
            "lesson_date": self.future,
            "poses": Pose.objects.all(),
            "price": "2000"
        }
        form1 = RegisterLessonForm(data=content1)
        form2 = RegisterLessonForm(data=content2)
        self.assertTrue(form1.is_valid())
        self.assertTrue(form2.is_valid())

    def test_register_past_lesson(self):
        content = {
            "style": "normal",
            "lesson_date": self.past,
            "poses": Pose.objects.all(),
            "price": "400"
        }
        form = RegisterLessonForm(data=content)
        self.assertFalse(form.is_valid())

    def test_register_far_future_lesson(self):
        content = {
            "style": "normal",
            "lesson_date": self.far_future,
            "poses": Pose.objects.all(),
            "price": "500"
        }
        form = RegisterLessonForm(data=content)
        self.assertFalse(form.is_valid())

    # Testing for style
    def test_register_unusable_style_lesson(self):
        content = {
            "style": "unusable",
            "lesson_date": self.future,
            "poses": Pose.objects.all(),
            "price": "300"
        }
        form = RegisterLessonForm(data=content)
        self.assertFalse(form.is_valid())
        
    def test_register_unusable_price_format(self):
        content = {
            "style": "normal",
            "lesson_date": self.future,
            "poses": Pose.objects.all(),
            "price": "testprice"
        }
        form = RegisterLessonForm(data=content)
        self.assertFalse(form.is_valid())

class Utils:
    
    @staticmethod
    def create_pose():
        name = Utils.generate_random_string(10)
        detail = Utils.generate_random_string(30)
        return Pose.objects.create(name=name, detail=detail)
    
    @staticmethod
    def create_pose_collection():
        pose1 = Utils.create_pose()
        pose2 = Utils.create_pose()
        collection = PoseCollection.objects.create()
        collection.poses.add(pose1)
        collection.poses.add(pose2)
        return collection

    @staticmethod
    def create_datetime_string(dt):
        # Convert datetime to %Y-%m-%dT%H:%M string
        st_date = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day) + "T" + str(dt.hour) + ":" + str(dt.minute)
        return st_date
    
    @staticmethod
    def generate_random_string(size=15):
        string = "abcdefghijklmnopqrstuvwxyz0123456789"
        random_string = ""
        for i in range(size):
            random_string += random.choice(string)
        return random_string