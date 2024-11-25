from django.db import models

class News(models.Model):
    NEWS_CHOICES = [
        ("News_to_come", "다가올 소식"),
        ("Last_news", "지난 소식")
    ]

    title = models.CharField(max_length=80)
    content = models.TextField()
    news_type = models.CharField(max_length=15, choices=NEWS_CHOICES)
    image = models.ImageField(upload_to='upload_filepath', blank=True, null=True)
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
