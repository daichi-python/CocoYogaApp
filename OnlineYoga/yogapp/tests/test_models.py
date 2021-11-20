from django.test import TestCase
from django.utils import timezone
from yogapp.models import Lesson, Purchase, LessonStyle, Question, Answer, Instructer, QuestionAndAnswer
from registration.models import User

import datetime


class LessonModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="testuser", password="purchase_test_0630", email="aaabbb@gmail.com")
        user2 = User.objects.create_user(username="testdaichi", password="test_inst_0630", email="hhhaaa@gmail.com")
        instructer = Instructer.objects.create(user=user, introduction="this is test instructer")
        instructer2 = Instructer.objects.create(user=user2, introduction="this is test instructer")
        self.lesson1 = Utils.create_lesson(20, instructer2)
        self.lesson2 = Utils.create_lesson(-1, instructer)
        self.lesson3 = Utils.create_lesson(1, instructer)
        self.lesson4 = Utils.create_lesson(0, instructer)

        Purchase.objects.create(user=user2, lesson=self.lesson2)
        Purchase.objects.create(user=user2, lesson=self.lesson3)


    def test_get_number_of_participants(self):
        lesson_count = self.lesson2.get_number_of_participants()
        self.assertEqual(lesson_count, 1)

    def test_get_number_of_participants_not_purchased(self):
        lesson_count = self.lesson1.get_number_of_participants()
        self.assertEqual(lesson_count, 0)
        
    def test_is_accessible_lesson(self):
        self.assertTrue(self.lesson4.is_accessible_lesson())
        
    def test_is_accessible_lesson_return_false(self):
        self.assertFalse(self.lesson3.is_accessible_lesson())


class Utils(object):
    @staticmethod
    def create_lesson(days, instructer):
        lesson_style = LessonStyle.objects.create(rank="normal", capacity=50)
        date = timezone.now() + datetime.timedelta(days)
        return Lesson.objects.create(lesson_date=date, style_id=lesson_style.id, instructer=instructer)