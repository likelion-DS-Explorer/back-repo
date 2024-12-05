from .models import Profile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
from clubs.models import Club, ClubUserRecord
from news.models import News
from recruit.models import ClubRecruit, RecruitApply

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    #is_manager = serializers.MultipleChoiceField(choices=Profile.CLUB_CHOICES)
    
    class Meta:
        model = Profile
        fields = ('email', 'password', 'nickname', 'name', 'major', 'student_id', 'cp_number', 'is_manager')
        extra_kwargs = {'email': {'required': True}}

    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 존재하는 이메일 주소입니다.")
        return value

    def create(self, validated_data):
        user = Profile.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            name=validated_data['name'],
            major=validated_data['major'],
            student_id=validated_data['student_id'],
            cp_number=validated_data['cp_number'],
            is_manager=validated_data['is_manager']
        )
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)
            return token
        raise serializers.ValidationError(
            {
                "error":"잘못된 이메일 또는 비밀번호입니다."
            }
        )

class ClubNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('full_name',)

# 프로필 정보 확인
class ProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    clubs = ClubNameSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('image', 'name', 'nickname', 'student_id', 'major', 'clubs', 'created_at', 'updated_at')

    # 닉네임 중복 검사
    def validate_nickname(self, value):
        request_user = self.instance
        
        # 다른 사용자의 닉네임과 중복되는지 확인
        if Profile.objects.filter(nickname=value).exclude(id=request_user.id).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임입니다.")
        
        return value

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.image = validated_data.get('image', instance.image)
        instance.student_id = validated_data.get('student_id', instance.student_id)
        instance.major = validated_data.get('major', instance.major)
        instance.email = validated_data.get('email', instance.email)
        instance.is_manager = validated_data.get('is_manager', instance.is_manager)
        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.save()
        return instance

# 수정 가능 게시물 조회
class editPostSerialzier(serializers.ModelSerializer):
    post_type = serializers.SerializerMethodField()
    club_title = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'post_type', 'title', 'club_title','status', 'created_at', 'updated_at']

    def get_club_title(self, obj):
        if isinstance(obj, ClubRecruit):
            return obj.club.code if obj.club else None
        elif isinstance(obj, News):
            return obj.club_code
        return None

    def get_post_type(self, obj):
        if hasattr(obj, 'news_type'):
            return '활동 소식'
        elif hasattr(obj, 'style'):
            return '모집 공고'
        return None

    def get_status(self, obj):
        now = timezone.now().date()
        if hasattr(obj, 'news_type'):
            return "공개"
        elif hasattr(obj, 'end_doc'):
            if obj.end_interview < now:
                return "모집 종료"
            else:
                return "공개"
        return "비공개"

    def get_title(self, obj):
        return obj.title

    def get_created_at(self, obj):
        return obj.created_at

    def get_updated_at(self, obj):
        return obj.updated_at

# 내가 속한 동아리
class UserClubSerializer(serializers.ModelSerializer):
    clubs = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['clubs']

    def get_clubs(self, obj):
        club_records = ClubUserRecord.objects.filter(user=obj).select_related('club')

        club_list = []
        for record in club_records:
            club = record.club
            club_list.append({
                'name': club.full_name,
                'code': club.code,
                'category':club.category,
                'status': '활동 중' if record.leave_date is None else '활동 종료',
                'join_date': self.format_date(record.join_date),
                'leave_date': self.format_date(record.leave_date) if record.leave_date else None,
                'role': self.get_role(obj, club)
            })

        return club_list

    def get_role(self, obj, club):
        return '운영진' if club.code in obj.is_manager else '회원'

    def format_date(self, date):
        if date:
            return date.strftime('%Y-%m-%d')
        return None

class applyClubSerializer(serializers.ModelSerializer):
    recruit = serializers.SerializerMethodField()

    class Meta:
        model = RecruitApply
        fields = ['recruit']

    def get_recruit(self, obj):
        apply_records = RecruitApply.objects.filter(user=obj).select_related('recruit__club')

        application_list = []
        for record in apply_records:
            recruit = record.recruit
            club = recruit.club if recruit else None
            application_list.append({
                'apply_date': self.format_date(record.created_at),
                'club_name': club.full_name if club else None,
                'recruit_title': recruit.title if recruit else None,
                'category': club.category if club else None,
                'apply_method': recruit.apply_method if recruit else None,
                'progress_status': self.get_progress_status(record),
                'result_date': self.get_result_date(recruit),
                'note': recruit.apply_process if recruit else None
            })

        return application_list

    def format_date(self, date):
        return date.strftime('%Y-%m-%d') if date else None

    def get_progress_status(self, record):
        return "진행 중"

    def get_result_date(self, recruit):
        return self.format_date(recruit.end_interview) if recruit else None