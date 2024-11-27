from django.shortcuts import render
from rest_framework import viewsets, status
from .models import News
from .permissions import IsManagerOrReadOnly
from .serializers import NewsSerializer, NewsCreateUpdateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    permission_classes = [IsManagerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return NewsSerializer
        return NewsCreateUpdateSerializer

    def get_queryset(self):
        return News.objects.all()

    def list(self, request, pk=None):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"message":"뉴스 조회에 성공하였습니다.", "result":serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "뉴스 등록에 성공하였습니다."
            return Response({"message": message, "result": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message":"뉴스 생성에 실패하였습니다.", "result":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        news = get_object_or_404(News, pk=pk)
        serializer = self.get_serializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "뉴스 수정에 성공했습니다."
            return Response({"message": message, "result": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "뉴스 수정에 실패했습니다.", "result": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, username=None, pk=None):
        news = get_object_or_404(News, pk=pk)
        news.delete()
        return Response({"message": "뉴스 삭제에 성공했습니다."}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"message": "뉴스 조회에 성공하였습니다.", "result": serializer.data},
            status=status.HTTP_200_OK
        )