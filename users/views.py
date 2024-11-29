from django.shortcuts import render
from .models import Profile, Inquiry
from rest_framework import generics, status, viewsets
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, InquirySerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# 회원가입 뷰
class RegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegisterSerializer

# 로그인 뷰
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({"message":"로그인 성공", "token":token.key}, status=status.HTTP_200_OK)

# 로그아웃 뷰
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)

# 프로필 
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'student_id'

    def get_object(self):
        student_id = self.kwargs.get('student_id')
        return get_object_or_404(Profile, student_id=student_id)

# 1:1 문의
class InquiryViewSet(viewsets.ModelViewSet):
    serializer_class = InquirySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "문의가 성공적으로 제출되었습니다! \n 운영진이 확인 후 빠르게 답변드리겠습니다. 감사합니다."
            return Response({"message": message, "result": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message":"문의 제출에 실패했습니다.", "result":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)