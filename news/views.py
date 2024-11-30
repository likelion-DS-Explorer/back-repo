from django.shortcuts import render
from rest_framework import viewsets, status
from .models import News
from .permissions import IsManagerOrReadOnly
from .serializers import NewsSerializer, NewsCreateUpdateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    permission_classes = [IsManagerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return NewsSerializer
        return NewsCreateUpdateSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            news = serializer.save(author=request.user)
            return Response({
                "message": "뉴스 등록에 성공하였습니다.",
                "result": NewsSerializer(news).data
            }, status=status.HTTP_201_CREATED)
        return Response({"message":"뉴스 생성에 실패하였습니다.", "result":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        news = self.get_object()
        serializer = self.get_serializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            news = serializer.save()
            return Response({
                "message": "뉴스 수정에 성공했습니다.",
                "result": NewsSerializer(news).data
            }, status=status.HTTP_200_OK)
        return Response({"message": "뉴스 수정에 실패했습니다.", "result": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        news = get_object_or_404(News, pk=pk)
        news.delete()
        return Response({"message": "뉴스 삭제에 성공했습니다."}, status=status.HTTP_200_OK)