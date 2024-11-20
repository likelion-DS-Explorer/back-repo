from django.db import models
import os
from uuid import uuid4
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator

def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("%Y%m%d")
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'


class Profile(AbstractUser):
    name = models.CharField(max_length=10)
    major = models.CharField(max_length=15)
    student_id = models.CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    nickname = models.CharField(max_length=50)
    cp_number = models.CharField(max_length=11, validators=[MinLengthValidator(11), MaxLengthValidator(11)])
    image = models.ImageField(upload_to='upload_filepath', default='default.png')

    def __str__(self):
        return f'{self.username}'

    def clean(self):
        super().clean()
        if len(str(student_id)) != 8:
            raise ValidationError({'student_id':'학번은 반드시 8자리여야 합니다.'})