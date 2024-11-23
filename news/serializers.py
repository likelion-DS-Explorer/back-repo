from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = News
        fields = ['id', 'news_type', 'title', 'content', 'image']