from rest_framework import serializers
from .models import *

class ClubSerializer(serializers.ModelSerializer):
    days = serializers.MultipleChoiceField(choices=Club.DAYS_CHOICES)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = '__all__'
        read_only_fields = ('likes_count', 'created_at', 'updated_at', 'is_liked')

    def create(self, validated_data):
        user = self.context["request"].user
        is_manager = user.is_manager

        if not is_manager:
            raise serializers.ValidationError("해당 동아리에 대해 동아리 탐험 글을 생성할 권한이 없습니다.")

        if Club.objects.filter(code=is_manager).exists():
            raise serializers.ValidationError("이미 해당 동아리의 탐험 글이 존재합니다.")

        validated_data["code"] = is_manager
        return super().create(validated_data)
    
    def get_is_liked(self, obj): # 좋아요 눌렀는지
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ClubLike.objects.filter(
                club = obj,
                user = request.user
            ).exists()
        return False

class ClubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['image', 'full_name', 'created_at', 'updated_at']
    
class ClubLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubLike
        fields = ['id', 'user', 'club', 'created_at']