from django.shortcuts import render
from .models import Profile
from rest_framework import generics,status
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# 회원가입 뷰
class RegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegisterSerializer

# 로그인 뷰
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username=request.data.get("username")
        password=request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            LoginSerializer(request, user)
            return Response({"message":"로그인 성공"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"사용자 이름 또는 비밀번호가 맞지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

# 프로필 
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'student_id'

    def get_object(self):
        student_id = self.kwargs.get('student_id')
        return get_object_or_404(Profile, student_id=student_id)