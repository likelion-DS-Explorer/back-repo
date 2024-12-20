from django.db import models
from django.contrib.auth import get_user_model
from clubs.models import Club

class ClubRecruitImage(models.Model):
    clubrecruit = models.ForeignKey('ClubRecruit', related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500)
    is_thumbnail = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.clubrecruit.title} - {self.image_url}"
    
class ClubRecruit(models.Model):
    STYLE_CHOICES = [
        ('project', '프로젝트 및 대외 활동'),
        ('study', '학습 및 연구'),
        ('networking', '친목 및 네트워킹')
    ]

    APPLY_METHOD_CHOICES = [
        ('online', '온라인 신청'),
        ('email', '이메일 접수'),
        ('offline', '오프라인 신청')
    ]

    APPLY_PROCESS_CHOICES = [
        ('only_doc', '서류 전형'),
        ('doc_interview', '서류 및 면접 전형'),
        ('only_interview', '면접 전형'),
        ('none', '별도 전형 없음')
    ]

    club = models.ForeignKey('clubs.Club', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='club')
    club_code = models.CharField(max_length=20, null=True, blank=True)

    club_field = models.CharField(max_length=100, null=True, blank=True)
    style = models.CharField(max_length=15, choices=STYLE_CHOICES)

    apply_method = models.CharField(max_length=15, choices=APPLY_METHOD_CHOICES)
    apply_process = models.CharField(max_length=15, choices=APPLY_PROCESS_CHOICES)
    start_doc = models.DateField()
    end_doc = models.DateField()
    start_interview = models.DateField()
    end_interview = models.DateField()
    recruit_result = models.DateField()

    form_link = models.URLField(blank=True, null=True)

    title = models.CharField(max_length=80)
    content = models.TextField(blank=True, null=True)

    scraps_count = models.PositiveBigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='recruit_author')

    def __str__(self):
        return f"{self.title} - {self.club_code} 공고"
    
    def save(self, *args, **kwargs):
        if self.club_code and not self.club:
            try:
                self.club = Club.objects.get(code=self.club_code)
            except Club.DoesNotExist:
                raise ValueError("해당 동아리 정보를 먼저 등록해야 합니다.")
        
        super().save(*args, **kwargs)
    
class RecruitScrap(models.Model):
    user = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name="scraped_recruit")
    recruit = models.ForeignKey('ClubRecruit', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recruit'], name='unique_user_recruit_scrap')
        ]

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            self.recruit.scraps_count += 1
        else:
            self.recruit.scraps_count -= 1
        self.recruit.save()

    def delete(self, *args, **kwargs):
        recruit = self.recruit
        super().delete(*args, **kwargs)
        recruit.scraps_count -= 1
        recruit.save()

    def __str__(self):
        return f"{self.user} → {self.recruit} 스크랩"

class RecruitApply(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recruit = models.ForeignKey('ClubRecruit', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recruit'], name='unique_user_recruit_apply')
        ]

    def __str__(self):
        return f"{self.user} → {self.recruit} 지원"