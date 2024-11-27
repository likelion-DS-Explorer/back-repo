from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
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