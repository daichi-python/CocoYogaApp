from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import Widget
from django.utils import timezone
from .models import LessonStyle, Pose

import datetime

QANDA_CATEGORIES = (
    ("1", "レッスンについて"),
    ("2", "インストラクターについて"),
    ("3", "要望"),
    ("4", "その他"),
)

STYLES = (
    ("normal", LessonStyle.objects.get(capacity=50)),
    ("premium", LessonStyle.objects.get(capacity=10)),
)

class QuestionAndAnswerForm(forms.Form):
    category = forms.ChoiceField(
        label="カテゴリ",
        choices=QANDA_CATEGORIES
    )
    detail = forms.CharField(
        label="お問い合わせ内容",
        widget=forms.Textarea(attrs={"placeholder": "10文字以上200文字以下で入力してください。"}),
    )

    def clean_detail(self):
        detail = self.cleaned_data["detail"]
        if 10 <= len(detail) <= 200:
            return detail
        raise ValidationError("10文字以上200文字以下になっていません。")
    

class AnswerForm(forms.Form):
    detail = forms.CharField(
        label="回答",
        widget=forms.Textarea(attrs={"placeholder": "10文字以上200文字以下で入力してください。"})
    )
    
    def clean_detail(self):
        detail = self.cleaned_data["detail"]
        if 10 <= len(detail) <= 200:
            return detail
        raise ValidationError("10文字以上200文字以下になっていません。")


class RegisterLessonForm(forms.Form):
    style = forms.ChoiceField(
        label="レッスンスタイル",
        choices=STYLES,
    )
    lesson_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    poses = forms.ModelMultipleChoiceField(
        Pose.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    price = forms.CharField(
        widget=forms.NumberInput(
            attrs={"placeholder": "例：500, 1000"}
        )
    )

    def clean_lesson_date(self):
        date = self.cleaned_data["lesson_date"]

        if not timezone.now() < date < timezone.now() + datetime.timedelta(days=365):
            self.add_error("lesson_date", "未来の日時を入力してください。")
            raise ValidationError("You can't register this lesson.")

        st_date = str(date.year) + "-" + str(date.month) + "-" + str(date.day) + "T" + str(date.hour) + ":" + str(date.minute)
        lesson_date = timezone.make_aware(datetime.datetime.strptime(st_date, "%Y-%m-%dT%H:%M"))
        return lesson_date
    
    def clean_price(self):
        usable = "1234567890"
        price = self.cleaned_data["price"]
        for chr in price:
            if not chr in usable:
                self.add_error("price", "正しいフォーマットで入力してください。")
                raise ValidationError("You use unusable format.")
        return price
    

class PoseCreateForm(forms.Form):
    pose_name = forms.CharField(
        label = "ポーズ名",
        widget=forms.TextInput(attrs={"placeholder": "20文字以内で入力してください。"})
    )
    
    pose_detail = forms.CharField(
        label = "ポーズ詳細",
        widget = forms.Textarea(),
    )   
    
    def clean_pose_name(self):
        pose = self.cleaned_data["pose_name"]
        
        if len(pose) > 20:
            raise ValidationError("文字数が20文字を超えています。")
        
        if len(Pose.objects.filter(name=pose)) != 0:
            raise ValidationError("このポーズは登録済みです。")
        
        return pose