from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import json
from pathlib import Path
from django.conf import settings

def load_club_choices():
    file_path = Path(settings.BASE_DIR) / 'club.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from {file_path}.")

# username을 email로 바꿈
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class Profile(AbstractUser):
    CLUB_CHOICES = [(item["code"], item["name"]) for item in load_club_choices()]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=10)
    major = models.CharField(max_length=15)
    student_id = models.CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)], unique=True)
    nickname = models.CharField(max_length=50)
    cp_number = models.CharField(max_length=11, validators=[MinLengthValidator(11), MaxLengthValidator(11)])
    image = models.ImageField(upload_to='upload_filepath', default='default.png')
    is_manager = models.CharField(max_length=20, blank=True, choices=CLUB_CHOICES)
    club = models.CharField(max_length=20, blank=True, choices=CLUB_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    club_recruit = models.ForeignKey('recruit.ClubRecruit', on_delete=models.SET_NULL, null=True, blank=True, related_name='club_recruit')
    news = models.ForeignKey('news.News', on_delete=models.SET_NULL, null=True, blank=True, related_name='club_news')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if len(str(self.student_id)) != 8:
            raise ValidationError({'student_id':'학번은 반드시 8자리여야 합니다.'})