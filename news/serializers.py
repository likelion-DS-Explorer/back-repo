from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = News
        fields = ['id', 'news_type', 'title', 'content', 'image', 'created_at', 'updated_at', 'is_draft']

class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'news_type', 'title', 'content', 'image', 'is_draft']