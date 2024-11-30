from django.db import models
from users.models import Profile

class News(models.Model):
    NEWS_CHOICES = [
        ("News_to_come", "다가올 소식"),
        ("Last_news", "지난 소식")
    ]

    title = models.CharField(max_length=80)
    content = models.TextField()
    news_type = models.CharField(max_length=15, choices=NEWS_CHOICES)
    image = models.ImageField(upload_to='upload_filepath', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='news')

    def __str__(self):
        return self.title
