from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

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
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=10)
    major = models.CharField(max_length=15)
    student_id = models.CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    nickname = models.CharField(max_length=50)
    cp_number = models.CharField(max_length=11, validators=[MinLengthValidator(11), MaxLengthValidator(11)])
    image = models.ImageField(upload_to='upload_filepath', default='default.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if len(str(self.student_id)) != 8:
            raise ValidationError({'student_id':'학번은 반드시 8자리여야 합니다.'})