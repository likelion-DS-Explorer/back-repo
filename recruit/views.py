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

class ClubRecruitViewSet(viewsets.ModelViewSet):
    queryset = ClubRecruit.objects.all()
    serializer_class = ClubRecruitSerializer
    permission_classes = [IsManagerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        is_manager_club = user.is_manager
        club_code = self.request.data.get("club_code")

        if club_code != is_manager_club:
            raise PermissionDenied("해당 동아리에 대해 모집 공고를 생성할 권한이 없습니다.")

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        recruit = self.get_object()

        if recruit.club_code != user.is_manager:
            raise PermissionDenied("해당 동아리에 대해 모집 공고를 수정할 권한이 없습니다.")
        
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        recruit = self.get_object()

        if recruit.club_code != user.is_manager:
            raise PermissionDenied("해당 동아리에 대해 모집 공고를 삭제할 권한이 없습니다.")
            
        recruit.delete()
        return Response({"message": "모집 공고가 삭제되었습니다."},
                        status=status.HTTP_204_NO_CONTENT)

    def list(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = ClubRecruitListSerializer(queryset, many=True)
        return Response({"message":"모집 공고 조회에 성공하였습니다.", "result":serializer.data}, status=status.HTTP_200_OK)

class RecruitScrapViewSet(viewsets.ModelViewSet):
    queryset = RecruitScrap.objects.all()
    serializer_class = RecruitScrapSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def scrap(self, request, pk=None):
        recruit = get_object_or_404(ClubRecruit, pk=pk)
        user = request.user

        try:
            existing_scrap = RecruitScrap.objects.get(user=user, recruit=recruit)
            existing_scrap.delete()
            message = "스크랩이 취소되었습니다."
            status_code = status.HTTP_200_OK
        except RecruitScrap.DoesNotExist:
            RecruitScrap.objects.create(user=user, recruit=recruit)
            message = "스크랩이 추가되었습니다."
            status_code = status.HTTP_201_CREATED

        recruit.refresh_from_db()
        return Response({"message": message, "scraps_count": recruit.scraps_count}, status=status_code)
    
class RecruitApplyViewSet(viewsets.ModelViewSet):
    queryset = RecruitApply.objects.all()
    serializer_class = RecruitApplySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        recruit = get_object_or_404(ClubRecruit, pk=pk)
        user = request.user

        try:
            existing_apply = RecruitApply.objects.get(user=user, recruit=recruit)
            message = "지원한 공고입니다."
            status_code = status.HTTP_200_OK
        except RecruitApply.DoesNotExist:
            RecruitApply.objects.create(user=user, recruit=recruit)
            message = "지원하였습니다."
            status_code = status.HTTP_201_CREATED

        recruit.refresh_from_db()
        return Response({"message": message}, status=status_code)