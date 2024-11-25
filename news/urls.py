from django.urls import path
from .views import NewsViewSet
from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = [
    path('', NewsViewSet.as_view({'get': 'list', 'post': 'create'}), name='news'),
    path('<int:pk>/', NewsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='news-deatil'),
]