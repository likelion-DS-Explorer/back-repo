from rest_framework import serializers
from .models import News, NewsImage

class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image']

class NewsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = ['id', 'news_type', 'title', 'content', 'images', 'created_at', 'updated_at']

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = News
        exclude = ['author']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        news = News.objects.create(**validated_data)
        for image in images[:8]:  # 최대 8개 이미지만 처리
            NewsImage.objects.create(news=news, image=image)
        return news

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)
        instance = super().update(instance, validated_data)
        if images is not None:
            instance.images.all().delete()
            for image in images[:8]:  # 최대 8개 이미지만 처리
                NewsImage.objects.create(news=instance, image=image)
        return instance