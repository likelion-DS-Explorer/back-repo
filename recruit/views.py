from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ClubRecruit
from .serializers import *

class ClubRecruitViewSet(viewsets.ModelViewSet):
    queryset = ClubRecruit.objects.all()
    serializer_class = ClubRecruitSerializer
    permission_classes = [AllowAny] # 테스트용

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

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
        return Response({"message": message, "scrap_count": recruit.scrap_count}, status=status_code)