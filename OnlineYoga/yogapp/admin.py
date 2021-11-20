from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Answer, Instructer, Lesson, LessonStyle, Purchase, Question, QuestionAndAnswer, Pose, PoseCollection

# Register your models here.
admin.site.register(Lesson)
admin.site.register(Purchase)
admin.site.register(LessonStyle)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionAndAnswer)
admin.site.register(Instructer)
admin.site.register(Pose)
admin.site.register(PoseCollection)
