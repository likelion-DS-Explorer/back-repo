from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = 'clubs'

router = SimpleRouter()
router.register('', ClubViewSet, basename='club')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/like/', ClubLikeViewSet.as_view({'post': 'like'}), name='club-like'),
]
