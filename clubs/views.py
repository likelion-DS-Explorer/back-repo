from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from news.permissions import IsManagerOrReadOnly
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.utils import timezone

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    # permission_classes = [AllowAny] # 테스트용
    permission_classes = [IsManagerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        is_manager_club = user.is_manager
        club_code = self.request.data.get("code")

        print(user)
        print(is_manager_club)
        print(club_code)

        if club_code != is_manager_club:
            raise PermissionDenied("해당 동아리에 대해 동아리 탐험 글을 생성할 권한이 없습니다.")

        if Club.objects.filter(code=club_code).exists():
            raise serializers.ValidationError("이미 해당 동아리의 탐험 글이 존재합니다.")

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        club = self.get_object()

        if club.code != user.is_manager:
            raise PermissionDenied("해당 동아리에 대해 동아리 탐험 글을 수정할 권한이 없습니다.")
        
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        club = self.get_object()

        if club.code != user.is_manager:
            raise PermissionDenied("해당 동아리에 대해 동아리 탐험 글을 삭제할 권한이 없습니다.")
        
                
        club.delete()
        return Response({"message": "동아리 탐험 글이 삭제되었습니다."},
                        status=status.HTTP_204_NO_CONTENT)

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

# 동아리원 추가
def add_member_to_club(user, club_code):
    club = Club.objects.get(code=club_code)
    ClubUserRecord.objects.create(user=user, club=club)
    user.clubs.add(club)
    user.save()
    return True

def check_user_membership(user, club_code):
    return user.clubs.filter(code=club_code).exists()

# 동아리원 삭제
def remove_member_from_club(user, club_code):
    club = Club.objects.get(code=club_code)
    ClubUserRecord.objects.filter(user=user, club=club, leave_date__isnull=True).update(leave_date=timezone.now())
    user.clubs.remove(club)
    user.save()

# 동아리원
class AddClubMemberView(viewsets.ModelViewSet):
    serializer_class = AddClubMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileViewSerializer
        return AddClubMemberSerializer

    def get_queryset(self):
        club_code = self.kwargs.get('club_code')
        club = Club.objects.get(code=club_code)
        return club.club_members.all()

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

    def destroy(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')  
        club_code = self.kwargs.get('club_code')

        try:
            user_to_remove = Profile.objects.get(student_id=student_id)
            club = Club.objects.get(code=club_code)
            
            if club_code not in request.user.is_manager:
                return Response({"error": "해당 동아리의 관리자가 아닙니다."}, status=status.HTTP_403_FORBIDDEN)

            if not check_user_membership(user_to_remove, club_code):
                return Response({"error": "해당 사용자는 이 동아리에 속해 있지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

            remove_member_from_club(user_to_remove, club_code)
            
            leave_record = ClubUserRecord.objects.filter(user=user_to_remove, club=club).latest('leave_date')
            
            return Response({
                "message": f"{user_to_remove.name}님을 동아리에서 제거했습니다.",
                "leave_date": leave_record.leave_date
            }, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"error": "해당 사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Club.DoesNotExist:
            return Response({"error": "해당 동아리를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)