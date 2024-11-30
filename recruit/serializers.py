from rest_framework import serializers
from .models import *
from datetime import date

class ClubRecruitSerializer(serializers.ModelSerializer):
    is_scrapped = serializers.SerializerMethodField()

    class Meta:
        model = ClubRecruit
        fields = '__all__'
        read_only_fields = ('likes_count', 'created_at', 'updated_at', 'is_scrapped')

    def create(self, validated_data):
        return ClubRecruit.objects.create(**validated_data)
    
    def get_is_scrapped(self, obj): # 스크랩 눌렀는지
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return RecruitScrap.objects.filter(
                recruit = obj,
                user = request.user
            ).exists()
        return False

class ClubRecruitListSerializer(serializers.ModelSerializer):
    d_day = serializers.SerializerMethodField()

    class Meta:
        model = ClubRecruit
        fields = ['image', 'title', 'category', 'style', 'frequency', 'created_at', 'updated_at', 'end_doc', 'd_day']

    def get_d_day(self, obj):
        d_day = (obj.end_doc - date.today()).days
        return d_day if d_day >=0 else "마감"
    
class RecruitScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitScrap
        fields = ['id', 'user', 'recruit', 'created_at']