from rest_framework import serializers
from .models import *
from datetime import date

class ClubRecruitSerializer(serializers.ModelSerializer):
    is_scrapped = serializers.SerializerMethodField()
    club_code = serializers.CharField()

    class Meta:
        model = ClubRecruit
        fields = '__all__'
        read_only_fields = ('likes_count', 'created_at', 'updated_at', 'is_scrapped', 'club', 'club_code', 'author')
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        user = self.context["request"].user
        is_manager = user.is_manager
        club_code = validated_data.get('club_code')

        print(validated_data)
        print(user)
        print(is_manager)
        print(club_code)

        if not is_manager:
            raise serializers.ValidationError("모집 공고를 생성할 권한이 없습니다.")

        # if is_manager != club_code:
        #     raise serializers.ValidationError("해당 동아리에 대한 권한이 없습니다.")
        
        try:
            club = Club.objects.get(code=club_code)
            validated_data['club'] = club
        except Club.DoesNotExist:
            raise serializers.ValidationError("해당 동아리 정보를 먼저 등록해야 합니다.")

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.club.code != user.is_manager:
            raise serializers.ValidationError("해당 공고를 수정할 권한이 없습니다.")
        validated_data.pop('club_code', None)
        return super().update(instance, validated_data)
    
    def delete(self, instance, validated_data):
        user = self.context['request'].user
        if instance.club.code != user.is_manager:
            raise serializers.ValidationError("해당 공고를 삭제할 권한이 없습니다.")
        validated_data.pop('club_code', None)
        return super().delete(instance, validated_data)
    
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
    category = serializers.CharField(source='club.category')
    frequency = serializers.CharField(source='club.frequency')
    name = serializers.CharField(source='club.full_name')

    class Meta:
        model = ClubRecruit
        fields = ['image','name', 'title', 'category', 'style', 'frequency', 'created_at', 'updated_at', 'end_doc', 'd_day']

    def get_d_day(self, obj):
        d_day = (obj.end_doc - date.today()).days
        return d_day if d_day >=0 else "마감"
    
class RecruitScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitScrap
        fields = ['id', 'user', 'recruit', 'created_at']