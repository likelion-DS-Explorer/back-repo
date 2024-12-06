from rest_framework import serializers
from .models import *
from datetime import date

class ClubRecruitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubRecruitImage
        fields = ['id', 'image_url', 'is_thumbnail']

class ClubRecruitSerializer(serializers.ModelSerializer):
    is_scrapped = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    club_code = serializers.CharField()
    club_field = serializers.CharField(required=False)
    images = ClubRecruitImageSerializer(many=True, read_only=True)
    image_urls = serializers.ListField(
        child=serializers.URLField(max_length=500), 
        write_only=True, 
        required=False
    )

    class Meta:
        model = ClubRecruit
        fields = '__all__'
        read_only_fields = ('likes_count', 'created_at', 'updated_at', 'is_scrapped', 'is_applied', 'club', 'club_code', 'images')

    def validate_image_urls(self, value):
        if len(value) > 8:
            raise serializers.ValidationError("최대 8개의 이미지만 등록할 수 있습니다.")
        return value
    
    def create(self, validated_data):
        user = self.context["request"].user
        is_manager = user.is_manager
        club_code = validated_data.get('club_code')
        club_field = validated_data.get('club_field', '').strip()
        image_urls = validated_data.pop('image_urls', [])

        if not is_manager:
            raise serializers.ValidationError("모집 공고를 생성할 권한이 없습니다.")

        try:
            club = Club.objects.get(code=club_code)
            validated_data['club'] = club
        except Club.DoesNotExist:
            raise serializers.ValidationError("해당 동아리 정보를 먼저 등록해야 합니다.")

        if club_field:
            club_field = [field.strip() for field in club_field.split(',') if field.strip()]
            if len(club_field) > 5:
                raise serializers.ValidationError("활동분야는 최대 5개까지 입력 가능합니다.")
            validated_data['club_field'] = ', '.join(club_field)

        clubrecruit = super().create(validated_data)

        for idx, image_url in enumerate(image_urls):
            ClubRecruitImage.objects.create(
                clubrecruit=clubrecruit, 
                image_url=image_url, 
                is_thumbnail=(idx == 0)
            )

        return clubrecruit
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.club.code != user.is_manager:
            raise serializers.ValidationError("해당 공고를 수정할 권한이 없습니다.")
        validated_data.pop('club_code', None)
    
        image_urls = validated_data.pop('image_urls', None)

        updated_clubrecruit = super().update(instance, validated_data)

        if image_urls is not None:
            existing_image_urls = list(updated_clubrecruit.images.values_list('image_url', flat=True))

            urls_to_add = [url for url in image_urls if url not in existing_image_urls]
            urls_to_remove = [url for url in existing_image_urls if url not in image_urls]

            updated_clubrecruit.images.filter(image_url__in=urls_to_remove).delete()

            if len(updated_clubrecruit.images.all()) + len(urls_to_add) > 8:
                raise serializers.ValidationError("최대 8개의 이미지만 등록할 수 있습니다.")

            for idx, image_url in enumerate(urls_to_add):
                ClubRecruitImage.objects.create(
                    clubrecruit=updated_clubrecruit, 
                    image_url=image_url, 
                    is_thumbnail=(updated_clubrecruit.images.count() == 0 and idx == 0)
                )
            
            updated_clubrecruit.save()

        return updated_clubrecruit
    
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

    def get_is_applied(self, obj): # 지원했는지
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return RecruitApply.objects.filter(
                recruit = obj,
                user = request.user
            ).exists()
        return False
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if 'club_field' in representation and representation['club_field']:
            club_field = representation['club_field']
            representation['club_field'] = [field.strip() for field in club_field.split(',') if field.strip()]
        else:
            representation['club_field'] = []

        return representation

class ClubRecruitListSerializer(serializers.ModelSerializer):
    d_day = serializers.SerializerMethodField()
    category = serializers.CharField(source='club.category')
    frequency = serializers.CharField(source='club.frequency')
    name = serializers.CharField(source='club.full_name')

    class Meta:
        model = ClubRecruit
        fields = ['name', 'title', 'category', 'style', 'frequency', 'created_at', 'updated_at', 'end_doc', 'd_day']

    def get_d_day(self, obj):
        d_day = (obj.end_doc - date.today()).days
        return d_day if d_day >=0 else "마감"
    
class RecruitScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitScrap
        fields = ['id', 'user', 'recruit', 'created_at']

class RecruitApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitScrap
        fields = ['id', 'user', 'recruit', 'created_at']