from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField

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
    CLUB_CHOICES = [
        ("솔바람", '솔바람'),
        ("SoulLy", 'SoulLy'),
        ("운향", "운향"),
        ("운현극예술 연구회", "운현극예술 연구회"),
        ("카들레아", "카들레아"),
        ("F.O.R.K", "F.O.R.K"),
        ("P.I.C.E", "P.I.C.E"),
        ("M.O.D.s", "M.O.D.s"),
        ("운산" , "운산"),
        ("FC Flora" ,"FC Flora"),
        ("하이클리어", "하이클리어"),
        ("BEAUTIFLY", "BEAUTIFLY"),
        ("Win Hands Down", "Win Hands Down"),
        ("ISSUE", "ISSUE"),
        ("열음", "열음"),
        ("예운", "예운"),
        ("운지문학회", "운지문학회"),
        ("한빛", "한빛"),
        ("필름소피", "필름소피"),
        ("두들링", "두들링"),
        ("멋쟁이 사자처럼", "멋쟁이 사자처럼"),
        ("덕불", "덕불"),
        ("데레사", "데레사"),
        ("CCC", "CCC"),
        ("RADIUS", "RADIUS"),
        ("FM419", "FM419"),
        ("자세히생각하라", "자세히생각하라"),
        ("이오", "이오"),
        ("덕성로타트랙", "덕성로타트랙"),
        ("KUSA","KUSA"),
        ("도담도담", "도담도담"),
        ("덕냥당", "덕냥당"),
        ("꽃신을신고", "꽃신을 신고")
    ]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=10)
    major = models.CharField(max_length=15)
    student_id = models.CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)], unique=True)
    nickname = models.CharField(max_length=50)
    cp_number = models.CharField(max_length=11, validators=[MinLengthValidator(11), MaxLengthValidator(11)])
    image = models.ImageField(upload_to='upload_filepath', default='default.png')
    is_manager = MultiSelectField(max_length=20, blank=True, choices=CLUB_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if len(str(self.student_id)) != 8:
            raise ValidationError({'student_id':'학번은 반드시 8자리여야 합니다.'})
            

class Inquiry(models.Model):
    CLUB_CHOICES = [
        ("솔바람", '솔바람'),
        ("SoulLy", 'SoulLy'),
        ("운향", "운향"),
        ("운현극예술 연구회", "운현극예술 연구회"),
        ("카들레아", "카들레아"),
        ("F.O.R.K", "F.O.R.K"),
        ("P.I.C.E", "P.I.C.E"),
        ("M.O.D.s", "M.O.D.s"),
        ("운산" , "운산"),
        ("FC Flora" ,"FC Flora"),
        ("하이클리어", "하이클리어"),
        ("BEAUTIFLY", "BEAUTIFLY"),
        ("Win Hands Down", "Win Hands Down"),
        ("ISSUE", "ISSUE"),
        ("열음", "열음"),
        ("예운", "예운"),
        ("운지문학회", "운지문학회"),
        ("한빛", "한빛"),
        ("필름소피", "필름소피"),
        ("두들링", "두들링"),
        ("멋쟁이 사자처럼", "멋쟁이 사자처럼"),
        ("덕불", "덕불"),
        ("데레사", "데레사"),
        ("CCC", "CCC"),
        ("RADIUS", "RADIUS"),
        ("FM419", "FM419"),
        ("자세히생각하라", "자세히생각하라"),
        ("이오", "이오"),
        ("덕성로타트랙", "덕성로타트랙"),
        ("KUSA","KUSA"),
        ("도담도담", "도담도담"),
        ("덕냥당", "덕냥당"),
        ("꽃신을신고", "꽃신을 신고")
    ]

    inquiryClub = models.CharField(max_length=20, choices=CLUB_CHOICES)
    content = models.TextField()