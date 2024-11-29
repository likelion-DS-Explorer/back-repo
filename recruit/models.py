from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model

class ClubRecruit(models.Model):
    CATEGORY_CHOICES = [
        ('music', '공연ꞏ음악'),
        ('sports', '스포츠ꞏ레저'),
        ('volunteer', '사회ꞏ봉사'),
        ('art', '예술ꞏ창작'),
        ('study', '학술ꞏ탐구'),
        ('religion', '종교'),
        ('gender', '젠더ꞏ페미니즘'),
        ('it', 'IT'),
        ('culture', '문화ꞏ전통'),
        ('etc', '기타')
    ]

    STYLE_CHOICES = [
        ('project', '프로젝트 및 대외 활동'),
        ('study', '학습 및 연구'),
        ('networking', '친목 및 네트워킹')
    ]

    DAYS_CHOICES = [
        ('mon', '월'),
        ('tue', '화'),
        ('wed', '수'),
        ('thu', '목'),
        ('fri', '금'),
        ('sat', '토'),
        ('sun', '일')
    ]

    FEE_TYPE_CHOICES = [
        ('yearly', '연간'),
        ('monthly', '월간'),
        ('one_time', '1회 납부')
    ]

    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    style = models.CharField(max_length=15, choices=STYLE_CHOICES)

    frequency = models.CharField(max_length=20)
    days = MultiSelectField(max_length=20, choices=DAYS_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    location = models.CharField(max_length=100)

    fee_type = models.CharField(max_length=15, choices=FEE_TYPE_CHOICES)
    fee = models.PositiveIntegerField()

    apply_method = models.CharField(max_length=20)
    apply_process = models.CharField(max_length=20)
    start_doc = models.DateField()
    end_doc = models.DateField()
    start_interview = models.DateField()
    end_interview = models.DateField()

    image = models.ImageField(upload_to='upload_filepath', default='default.png')
    title = models.CharField(max_length=80)
    content = models.TextField()

    scrap_count = models.PositiveBigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class RecruitScrap(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recruit = models.ForeignKey('ClubRecruit', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recruit'], name='unique_user_recruit')
        ]

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            self.recruit.scrap_count += 1
        else:
            self.recruit.scrap_count -= 1
        self.recruit.save()

    def delete(self, *args, **kwargs):
        recruit = self.recruit
        super().delete(*args, **kwargs)
        recruit.scrap_count -= 1
        recruit.save()

    def __str__(self):
        return f"{self.user} → {self.recruit} 스크랩"