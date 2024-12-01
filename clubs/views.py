from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from news.permissions import IsManagerOrReadOnly
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    # permission_classes = [AllowAny] # 테스트용
    permission_classes = [IsManagerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        is_manager_club = user.is_manager
        club_name = self.request.data.get("name")

        print(user)
        print(is_manager_club)
        print(club_name)

        if club_name != is_manager_club:
            raise serializers.ValidationError("해당 동아리에 대해 동아리 탐험 글을 생성할 권한이 없습니다.")

        if Club.objects.filter(is_manager_club=club_name).exists():
            raise serializers.ValidationError("이미 해당 동아리의 탐험 글이 존재합니다.")

    def perform_update(self, serializer):
        user = self.request.user
        club = self.get_object()

        if club.name != user.is_manager:
            raise serializers.ValidationError("해당 동아리에 대해 동아리 탐험 글을 생성할 권한이 없습니다.")
        
        serializer.save()

    def list(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = ClubListSerializer(queryset, many=True)
        return Response({"message":"동아리 정보 조회에 성공하였습니다.", "result":serializer.data}, status=status.HTTP_200_OK)

class ClubLikeViewSet(viewsets.ModelViewSet):
    queryset = ClubLike.objects.all()
    serializer_class = ClubLikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        club = get_object_or_404(Club, pk=pk)
        user = request.user

        try:
            existing_like = ClubLike.objects.get(user=user, club=club)
            existing_like.delete()
            message = "좋아요가 취소되었습니다."
            status_code = status.HTTP_200_OK
        except ClubLike.DoesNotExist:
            ClubLike.objects.create(user=user, club=club)
            message = "좋아요가 추가되었습니다."
            status_code = status.HTTP_201_CREATED

        club.refresh_from_db()
        return Response({"message": message, "likes_count": club.likes_count}, status=status_code)

def check_user_membership(user, club_code):
    return club_code in user.club.split(',') if user.club else False

def add_member_to_club(user, club_code):
    if user.club:
        user.club += f",{club_code}"
    else:
        user.club = club_code
    user.save()
    return True

# 동아리원 추가
class AddClubMemberView(viewsets.ModelViewSet):
    serializer_class = AddClubMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileViewSerializer
        return AddClubMemberSerializer

    def get_queryset(self):
        club_code = self.kwargs.get('club_code')
        return Profile.objects.filter(club=club_code)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"message": "동아리원 조회에 성공하였습니다.", "result": serializer.data},
            status=status.HTTP_200_OK
        )

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

        if check_user_membership(user_to_add, club_code):
            return Response({"error": "이미 동아리원입니다."}, status=status.HTTP_400_BAD_REQUEST)

        success = add_member_to_club(user_to_add, club_code)

        return Response({"message": f"{user_to_add.name}님을 동아리원으로 추가했습니다."}, status=status.HTTP_201_CREATED)