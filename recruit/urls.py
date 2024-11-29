from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = 'recruit'

router = SimpleRouter()
router.register('', ClubRecruitViewSet, basename='club-recruit')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/scrap/', RecruitScrapViewSet.as_view({'post': 'scrap'}), name='recruit-scrap'),
]
