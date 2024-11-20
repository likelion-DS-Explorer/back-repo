from .models import Profile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

# 회원가입
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        write_only=True,
        required=True,
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators = [validate_password]
    )

    nickname = serializers.CharField(required=True)
    
    class Meta:
        model = Profile
        fields = ('email', 'password','nickname','name', 'major', 'student_id', 'cp_number')

    # 닉네임 중복 검사
    def validate_nickname(self, value):
        if Profile.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임입니다.")
        return value

    # 이메일 중복 검사
    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 존재하는 이메일 주소입니다.")
        return value

    def create(self, validated_data):
        user = Profile.objects.create(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            name=validated_data['name'],
            major=validated_data['major'],
            student_id=validated_data['student_id'],
            cp_number=validated_data['cp_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# 로그인
class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# 프로필 정보 확인
class ProfileSerializer(serializers.ModelField):
    class Meta:
        model = Profile
        fields = ('image', 'nickname', 'student_id', 'major', '')
