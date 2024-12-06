from rest_framework import serializers
from .models import *
from users.models import Profile

class ClubImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubImage
        fields = ['id', 'image_url', 'is_thumbnail']

class ClubSerializer(serializers.ModelSerializer):
    days = serializers.MultipleChoiceField(choices=Club.DAYS_CHOICES)
    is_liked = serializers.SerializerMethodField()
    images = ClubImageSerializer(many=True, read_only=True)
    image_urls = serializers.ListField(
        child=serializers.URLField(max_length=500), 
        write_only=True, 
        required=False
    )

    class Meta:
        model = Club
        fields = '__all__'
        read_only_fields = ('likes_count', 'created_at', 'updated_at', 'is_liked', 'images')
    
    def validate_image_urls(self, value):
        if len(value) > 8:
            raise serializers.ValidationError("최대 8개의 이미지만 등록할 수 있습니다.")
        return value
    
    def create(self, validated_data):
        user = self.context["request"].user
        is_manager = user.is_manager
        code = validated_data.get('code')
        image_urls = validated_data.pop('image_urls', [])

        if not is_manager:
            raise serializers.ValidationError("동아리 탐험 글을 생성할 권한이 없습니다.")

        if Club.objects.filter(code=is_manager).exists():
            raise serializers.ValidationError("이미 해당 동아리의 탐험 글이 존재합니다.")

        club = super().create(validated_data)

        for idx, image_url in enumerate(image_urls):
            ClubImage.objects.create(
                club=club, 
                image_url=image_url, 
                is_thumbnail=(idx == 0)
            )

        return club
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.code != user.is_manager:
            raise serializers.ValidationError("해당 동아리의 탐험 글을 수정할 권한이 없습니다.")
        
        image_urls = validated_data.pop('image_urls', None)

        updated_club = super().update(instance, validated_data)

        if image_urls is not None:
            existing_image_urls = list(updated_club.images.values_list('image_url', flat=True))

            urls_to_add = [url for url in image_urls if url not in existing_image_urls]
            urls_to_remove = [url for url in existing_image_urls if url not in image_urls]

            updated_club.images.filter(image_url__in=urls_to_remove).delete()

            if len(updated_club.images.all()) + len(urls_to_add) > 8:
                raise serializers.ValidationError("최대 8개의 이미지만 등록할 수 있습니다.")

            for idx, image_url in enumerate(urls_to_add):
                ClubImage.objects.create(
                    club=updated_club, 
                    image_url=image_url, 
                    is_thumbnail=(updated_club.images.count() == 0 and idx == 0)
                )
            
            updated_club.save()

        return updated_club
        

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
        fields = ['full_name', 'created_at', 'updated_at']
    
class ClubLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubLike
        fields = ['id', 'user', 'club', 'created_at']

# 동아리원 추가
class AddClubMemberSerializer(serializers.Serializer):
    search_type = serializers.ChoiceField(choices=[('name', '이름'), ('student_id', '학번')])
    search_term = serializers.CharField()
    club_code = serializers.ChoiceField(choices=Profile.CLUB_CHOICES)
    leave_date = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)

    def validate_club_code(self, value):
        valid_codes = [choice[0] for choice in Profile.CLUB_CHOICES]
        if value not in valid_codes:
            raise serializers.ValidationError("유효하지 않은 동아리 코드입니다.")
        return value

    def validate_leave_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("탈퇴 날짜는 현재 날짜보다 이전일 수 없습니다.")
        return value

class ProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'student_id')