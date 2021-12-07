from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.forms.models import model_to_dict
from django.utils import timezone

import datetime

# Create your models here.
class Instructer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("registration.User", on_delete=CASCADE, related_name="instructer_user")
    introduction = models.TextField()
    created = models.DateTimeField("create date", auto_now_add=True)
    updated = models.DateTimeField("update date", auto_now=True)

    def __str__(self):
        return self.user.username


class Pose(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    detail = models.TextField()

    def __str__(self):
        return self.name


class PoseCollection(models.Model):
    id = models.AutoField(primary_key=True)
    poses = models.ManyToManyField(Pose)


class LessonStyle(models.Model):
    id = models.AutoField(primary_key=True)
    rank = models.CharField(max_length=10, choices=(("normal", "ノーマル"), ("premium", "プレミアム")))
    capacity = models.IntegerField(default=50)
    created = models.DateTimeField("create date", auto_now_add=True)
    updated = models.DateTimeField("update date", auto_now=True)

    def __str__(self):
        return self.get_rank_display()


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    style = models.ForeignKey(LessonStyle, on_delete=PROTECT, related_name="lesson_style")
    instructer = models.ForeignKey(Instructer, on_delete=CASCADE, related_name="instructer")
    whereby = models.CharField(max_length=80, default="this lesson is not active")
    poses = models.ForeignKey(PoseCollection, on_delete=CASCADE, related_name="pose_collection", null=True)
    price = models.IntegerField(default=1000)
    lesson_date = models.DateTimeField("lesson date")
    created = models.DateTimeField("create date", auto_now_add=True)
    updated = models.DateTimeField("update date", auto_now=True)

    def __str__(self):
        return self.instructer.user.username + "-" + str(self.lesson_date)

    def is_past_lesson(self):
        """
        Return True for past lessons.
        """
        return self.lesson_date < timezone.now()
    
    def is_accessible_lesson(self):
        """
        If there is a lesson between 5 minutes ago and 1 hour later, return True.
        """
        return self.lesson_date - datetime.timedelta(minutes=5) < timezone.now() < self.lesson_date + datetime.timedelta(hours=1)

    def get_number_of_participants(self):
        return Purchase.objects.filter(lesson=self).count()


class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("registration.User", on_delete=CASCADE, related_name="purchase_user")
    lesson = models.ForeignKey(Lesson, on_delete=CASCADE, related_name="purchased_lesson")
    purchased = models.DateTimeField("create date", auto_now_add=True)
    stripe_id = models.CharField("stripe", max_length=200, null=True)
    updated = models.DateTimeField("update date", auto_now=True)
    
    def __str__(self):
        return "{} {}".format(self.user.username, self.lesson.lesson_date)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("registration.User",on_delete=PROTECT , related_name="posted_user")
    category = models.CharField(max_length=10, choices=(
        ("1", "レッスンについて"), ("2", "インストラクターについて"), ("3", "要望"), ("4", "その他")
        ))
    detail = models.TextField()
    is_answerd = models.BooleanField("is answerd", default=False)
    created = models.DateTimeField("create date", auto_now_add=True)
    updated = models.DateTimeField("update date", auto_now=True)
    
    def __str__(self):
        return self.get_category_display()


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    instructer = models.ForeignKey(Instructer, on_delete=PROTECT, related_name="answered_instructer")
    detail = models.TextField()
    created = models.DateTimeField("create date", auto_now_add=True)
    updated = models.DateTimeField("update date", auto_now=True)
    
    def __str__(self):
        return self.detail[:10]


class QuestionAndAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=CASCADE, related_name="question")
    answer = models.ForeignKey(Answer, on_delete=CASCADE, related_name="answer")
    created = models.DateTimeField("create date", auto_now_add=True)
    updated = models.DateTimeField("update date", auto_now=True)