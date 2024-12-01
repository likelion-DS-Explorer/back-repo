from django.shortcuts import render
from .models import Profile
from rest_framework import generics, status, viewsets
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, editPostSerialzier, AddClubMemberSerializer
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from news.permissions import IsManagerOrReadOnly
from news.models import News
from recruit.models import ClubRecruit

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

# 수정 가능 게시글 조회
class editPostViewset(viewsets.ModelViewSet):
    permission_classes = [IsManagerOrReadOnly]
    serializer_class = editPostSerialzier
    lookup_field = 'student_id'

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        user = get_object_or_404(Profile, student_id=student_id)

        news = News.objects.filter(author=user)
        recruits = ClubRecruit.objects.filter(author=user)
        if not news.exists() and not recruits.exists():
            return Response(
            {"error": "관련 게시글이 존재하지 않습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    
        return list(news) + list(recruits)

    def list(self, request, student_id=None):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(
            {"message": "수정 가능 게시글 조회에 성공하였습니다.", "result": serializer.data},
            status=status.HTTP_200_OK
        )


# 동아리원 추가
class AddClubMemberView(generics.CreateAPIView):
    serializer_class = AddClubMemberSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        search_type = serializer.validated_data['search_type']
        search_term = serializer.validated_data['search_term']
        club_code = serializer.validated_data['club_code']

        try:
            if search_type == 'name':
                user_to_add = Profile.objects.get(name=search_term)
            else:  # student_id
                user_to_add = Profile.objects.get(student_id=search_term)
            
            club_name = dict(Profile.CLUB_CHOICES).get(club_code)
        except Profile.DoesNotExist:
            if search_type == 'name':
                error_message = "해당 이름의 사용자를 찾을 수 없습니다."
            else:
                error_message = "해당 학번의 사용자를 찾을 수 없습니다."
            return Response({"error": error_message}, status=status.HTTP_404_NOT_FOUND)
            
            if not club_name:
                return Response({"error": "해당 코드의 동아리를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if club_code not in request.user.is_manager:
            return Response({"error": "해당 동아리의 관리자가 아닙니다."}, status=status.HTTP_403_FORBIDDEN)

        if user_to_add.club:
            user_to_add.club += f",{club_code}"
        else:
            user_to_add.club = club_code
        user_to_add.save()

        return Response({"message": f"{user_to_add.name}님을 동아리원으로 추가했습니다."}, status=status.HTTP_201_CREATED)