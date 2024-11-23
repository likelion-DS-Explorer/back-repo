from django.db import models

class News(models.Model):
    NEWS_CHOICES = [
        ("News_to_come", "다가올 소식"),
        ("Last_news", "지난 소식")
    ]

    title = models.CharField(max_length=80)
    content = models.TextField()
    news_type = models.CharField(max_length=15, choices=NEWS_CHOICES)

    def __str__(self):
        return self.title
