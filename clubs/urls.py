from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = 'clubs'

router = SimpleRouter()
router.register('', ClubViewSet, basename='club')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/like/', ClubLikeViewSet.as_view({'post': 'like'}), name='club-like'),
    path('<str:club_code>/members/', AddClubMemberView.as_view({'get': 'list', 'post': 'create'}), name='club-members'),
    path('<str:club_code>/members/<str:student_id>/', AddClubMemberView.as_view({'delete': 'destroy'}), name='club-member-delete')
]
