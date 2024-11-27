from rest_framework import serializers
from .models import ClubRecruit

class ClubRecruitSerializer(serializers.Serializer):
    class Meta:
        model = ClubRecruit
        fields = '__all__'

class ClubRecruitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubRecruit
        fields = '__all__'