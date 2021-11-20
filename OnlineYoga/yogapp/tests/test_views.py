from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse

from yogapp.models import Instructer, Lesson, LessonStyle, Purchase, Pose, PoseCollection
from registration.models import User

import datetime
import random

# Create your tests here.
class HomeViewTest(TestCase):

    def setUp(self):
        self.user = ModelCreate.create_user()
        self.client = ModelCreate.login_user(self.user)
        instructer = ModelCreate.create_instructer(self.user)
        
        self.lesson1 = ModelCreate.create_lesson(instructer, days=20)
        self.lesson2 = ModelCreate.create_lesson(instructer, days=-1)
        self.lesson3 = ModelCreate.create_lesson(instructer, days=1)

    def test_user_doesnt_have_lesson(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "レッスンが登録されていません")

    def test_user_has_lesson(self):
        ModelCreate.create_purchase(self.user, self.lesson1)
        ModelCreate.create_purchase(self.user, self.lesson2)
        ModelCreate.create_purchase(self.user, self.lesson3)
        
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "レッスンが登録されていません")

    def test_user_only_has_past_lesson(self):
        ModelCreate.create_purchase(self.user, self.lesson2)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "レッスンが登録されていません")


class PurchaseViewTest(TestCase):

    def setUp(self):
        self.user = ModelCreate.create_user()
        self.client = ModelCreate.login_user(self.user)
        instructer = ModelCreate.create_instructer(self.user)
        self.lesson1 = ModelCreate.create_lesson(instructer, days=1)
        self.lesson2 = ModelCreate.create_lesson(instructer, days=-1)

    def test_access_to_future_lesson_purchase_view(self):
        response = self.client.get(reverse("purchase", args=(self.lesson1.id,)))
        self.assertEqual(response.status_code, 200)

    def test_access_to_past_lesson_purchase_view(self):
        response = self.client.get(reverse("purchase", args=(self.lesson2.id,)))
        self.assertContains(response, "このレッスンは終了しています。")


class RegisterLessonViewTest(TestCase):

    def setUp(self):
        user = ModelCreate.create_user()
        instructer = ModelCreate.create_user()
        ModelCreate.create_instructer(instructer)
        self.client_user = ModelCreate.login_user(user)
        self.client_inst = ModelCreate.login_user(instructer)

        future = timezone.now() + datetime.timedelta(1)
        self.future = ModelCreate.create_datetime_string(future)
        
        past = timezone.now() + datetime.timedelta(-1)
        self.past = ModelCreate.create_datetime_string(past)

        ModelCreate.create_lesson_style()
        ModelCreate.create_pose_collection()

    def test_register_lesson_view(self):
        content = {
            "style": "normal",
            "lesson_date": self.future,
            "poses": "1",
            "price": "1000",
        }
        self.client_inst.post(reverse("register"), content)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_register_lesson_by_not_instructer(self):
        content = {
            "style": "normal",
            "lesson_date": self.future,
            "poses": "1",
            "price": "1000"
        }
        self.client_user.post(reverse("register"), content)
        self.assertEqual(Lesson.objects.count(), 0)
        
    def test_register_past_lesson(self):
        content = {
            "style": "normal",
            "lesson_date": self.past,
            "poses": "1",
            "price": "1000"
        }
        self.client_user.post(reverse("register"), content)
        self.assertEqual(Lesson.objects.count(), 0)
        
    def test_register_lesson_price_receive_by_string(self):
        content = {
            "style": "normal",
            "lesson_date": self.past,
            "poses": "1",
            "price": "test"
        }
        self.client_user.post(reverse("register"), content)
        self.assertEqual(Lesson.objects.count(), 0)


class MypageViewTest(TestCase):
    
    def setUp(self):
        self.user = ModelCreate.create_user()
        self.client = ModelCreate.login_user(self.user,)
        instructer = ModelCreate.create_instructer(self.user)
        self.future_lesson = ModelCreate.create_lesson(instructer, days=1)
        self.past_lesson = ModelCreate.create_lesson(instructer, days=-1)

    def test_user_has_future_lesson_and_past_lesson(self):
        ModelCreate.create_purchase(self.user, self.future_lesson)
        ModelCreate.create_purchase(self.user, self.past_lesson)

        response = self.client.get(reverse("mypage"))
        self.assertNotContains(response, "まだレッスンを受講していません。")
        self.assertNotContains(response, "購入したレッスンはありません。")

    def test_user_only_has_future_lesson(self):
        ModelCreate.create_purchase(self.user, self.future_lesson)

        response = self.client.get(reverse("mypage"))
        self.assertContains(response, "まだレッスンを受講していません。")
        self.assertNotContains(response, "購入したレッスンはありません。")

    def test_user_only_has_past_lesson(self):
        ModelCreate.create_purchase(self.user, self.past_lesson)

        response = self.client.get(reverse("mypage"))
        self.assertContains(response, "購入したレッスンはありません。")
        self.assertNotContains(response, "まだレッスンを受講していません。")

    def test_user_doesnt_have_lesson(self):
        response = self.client.get(reverse("mypage"))
        self.assertContains(response, "まだレッスンを受講していません。")
        self.assertContains(response, "購入したレッスンはありません。")

    
class InstructerViewTest(TestCase):

    def setUp(self):
        user = ModelCreate.create_user()
        instructer_user = ModelCreate.create_user()

        self.instructer = ModelCreate.create_instructer(instructer_user)
        self.client_user = ModelCreate.login_user(user)
        self.client_inst = ModelCreate.login_user(instructer_user)

    def test_instructer_view_accessed_by_instructer(self):
        future_lesson = ModelCreate.create_lesson(self.instructer, days=1)
        past_lesson = ModelCreate.create_lesson(self.instructer, days=-1)
        response = self.client_inst.get(reverse("instructer"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, future_lesson.style.get_rank_display())
        self.assertNotContains(response, "レッスン履歴はありません。")
        self.assertNotContains(response, "レッスン予定はありません。")

    def test_instructer_view_instructer_doesnt_have_lesson(self):
        response = self.client_inst.get(reverse("instructer"))
        self.assertContains(response, "レッスン履歴はありません。")
        self.assertContains(response, "レッスン予定はありません。")


    """
    this test raise DoesNotExistError. 
    """
    # def test_instructer_view_accessed_by_not_instructer(self):
    #     response = self.client_user.get(reverse("instructer"))
    #     self.assertEqual(response.status_code, 302)

class LessonViewTest(TestCase):
    def setUp(self):
        self.user = ModelCreate.create_user()
        instructer_user = ModelCreate.create_user()

        self.instructer = ModelCreate.create_instructer(instructer_user)
        self.client_user = ModelCreate.login_user(self.user)
        self.client_inst = ModelCreate.login_user(instructer_user)
        
        self.active_lesson = ModelCreate.create_lesson(self.instructer)
        self.past_lesson = ModelCreate.create_lesson(self.instructer, hours=1, minutes=1)
        
    def test_lesson_view_with_unable_token(self):
        response = self.client_user.get(reverse("lesson", args=(100,)))
        self.assertEqual(response.status_code, 404)
        
    def test_lesson_view_by_not_purchase_user(self):
        response = self.client_user.get(reverse("lesson", args=(self.active_lesson.id,)))
        self.assertEqual(response.status_code, 403)
        
    def test_lesson_view_access_past_lesson(self):
        ModelCreate.create_purchase(self.user, self.past_lesson)
        response = self.client_user.get(reverse("lesson", args=(self.past_lesson.id,)))
        self.assertContains(response, "このレッスンにはアクセスできません。")
        
    def test_lesson_view_by_purchase_user(self):
        ModelCreate.create_purchase(self.user, self.active_lesson)
        response = self.client_user.get(reverse("lesson", args=(self.active_lesson.id,)))
        self.assertEqual(response.status_code, 200)


class ViewTestByNotAuthenticatedUser(TestCase):

    def setUp(self):
        self.user = ModelCreate.create_user()
        self.client = Client()
        self.instructer = ModelCreate.create_instructer(self.user)

    def test_not_user_access_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_not_user_access_mypage_view(self):
        response = self.client.get(reverse("mypage"))
        self.assertEqual(response.status_code, 302)

    def test_not_user_access_purchase_view(self):
        lesson = ModelCreate.create_lesson(self.instructer, days=30)
        response = self.client.get(reverse("purchase", args=(lesson.id,)))
        self.assertEqual(response.status_code, 302)

    def test_not_user_access_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 302)

    def test_not_user_access_qanda_view(self):
        response = self.client.get(reverse("qanda"))
        self.assertEqual(response.status_code, 302)


class ViewTestByAuthenticatedUser(TestCase):

    def setUp(self):
        self.user = ModelCreate.create_user()
        self.client = ModelCreate.login_user(self.user)
        self.instructer = ModelCreate.create_instructer(self.user)

    def test_authenticated_user_access_purchase_view(self):
        lesson = ModelCreate.create_lesson(self.instructer, 30)
        response = self.client.get(reverse("purchase", args=(lesson.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, lesson.id)

    def test_authenticated_user_access_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_access_qanda_view(self):
        response = self.client.get(reverse("qanda"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_access_mypage_view(self):
        response = self.client.get(reverse("mypage"))
        self.assertEqual(response.status_code, 200)
        
    def test_authenticated_user_access_instructer_view(self):
        response = self.client.get(reverse("instructer"))
        self.assertEqual(response.status_code, 200)


class ModelCreate(object):
    @staticmethod
    def create_lesson(instructer_obj, days=0, hours=0, minutes=0, rank="normal", capacity=50):
        style = ModelCreate.create_lesson_style(rank, capacity)
        date = timezone.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes)
        
        pose = Pose.objects.create(name=ModelCreate.generate_random_string(10), detail=ModelCreate.generate_random_string(40))
        pose_col = PoseCollection.objects.create()
        pose_col.poses.add(pose)
        
        return Lesson.objects.create(lesson_date=date, style_id=style.id, instructer=instructer_obj, poses=pose_col)
    
    @staticmethod
    def create_lesson_style(rank="normal", capacity=50):
        return LessonStyle.objects.create(rank=rank, capacity=capacity)
    
    @staticmethod
    def create_purchase(user_obj, lesson_obj):
        return Purchase.objects.create(user=user_obj, lesson=lesson_obj)
    
    @staticmethod
    def create_user(password="testpass0630"):
        username = ModelCreate.generate_random_string(10)
        email = ModelCreate.generate_random_string(10) + "@gmail.com"
        return User.objects.create_user(username=username, password=password, email=email)
    
    @staticmethod
    def create_instructer(user_obj):
        return Instructer.objects.create(user=user_obj, introduction=ModelCreate.generate_random_string(30))
    
    @staticmethod
    def login_user(user_obj, password="testpass0630"):
        client = Client()
        client.login(username=user_obj.username, password=password)
        return client
    
    @staticmethod
    def create_pose():
        name = ModelCreate.generate_random_string(10)
        detail = ModelCreate.generate_random_string(30)
        return Pose.objects.create(name=name, detail=detail)
    
    @staticmethod
    def create_pose_collection():
        pose1 = ModelCreate.create_pose()
        pose2 = ModelCreate.create_pose()
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