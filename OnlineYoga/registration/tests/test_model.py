from django.test import TestCase
from django.utils import timezone
from registration.models import User
from yogapp.models import Instructer, Pose, PoseCollection, Lesson, LessonStyle, Purchase

import datetime
import random

class TestUserModel(TestCase):
    
    def setUp(self):
        self.user = ModelCreate.create_user()
        self.instructer = ModelCreate.create_user()
        inst = ModelCreate.create_instructer(self.instructer)
        self.lesson = ModelCreate.create_lesson(inst)

    def test_is_instructer(self):
        self.assertTrue(self.instructer.is_instructer())

    def test_is_instructer_by_not_instructer(self):
        self.assertFalse(self.user.is_instructer())
        
    def test_does_user_have_lesson(self):
        ModelCreate.create_purchase(self.user, self.lesson)
        self.assertTrue(self.user.does_user_have_lesson(self.lesson))
        
    def test_does_not_user_have_lesson(self):
        self.assertFalse(self.user.does_user_have_lesson(self.lesson))
    
    
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