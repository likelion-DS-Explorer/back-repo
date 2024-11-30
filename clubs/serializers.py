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
        return Club.objects.create(**validated_data)
    
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
        fields = ['image', 'name', 'created_at', 'updated_at']
    
class ClubLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubLike
        fields = ['id', 'user', 'club', 'created_at']