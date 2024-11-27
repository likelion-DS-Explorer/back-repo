from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import ClubRecruit
from .serializers import ClubRecruitSerializer

class ClubRecruitViewSet(viewsets.ModelViewSet):
    queryset = ClubRecruit.objects.all()
    serializer_class = ClubRecruitSerializer
    permission_classes = [AllowAny] # 테스트용

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()