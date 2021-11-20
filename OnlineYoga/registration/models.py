from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from yogapp.models import Instructer, Purchase

# Create your models here.
class User(AbstractUser):
    sex = models.CharField("性別", max_length=5, choices=(("man", "男性"), ("woman", "女性")), null=True, name="sex")
    birthday = models.DateField("誕生日", name="birthday", null=True)

    def is_instructer(self):
        instructer = Instructer.objects.filter(user=self)
        return len(instructer) == 1
    
    def does_user_have_lesson(self, lesson):
        my_lesson = Purchase.objects.filter(user=self).filter(lesson=lesson)
        return len(my_lesson) == 1