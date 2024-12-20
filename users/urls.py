from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:student_id>/', ProfileView.as_view()),
    path('profile/<str:student_id>/edit-posts/', editPostViewset.as_view({'get':'list'}), name='edit_post_list'),
    path('profile/<str:student_id>/affiliated-clubs/', UserClubsView.as_view(), name='affiliated-clubs'),
    path('profile/<str:student_id>/apply/', ApplyClubsView.as_view(), name='apply-clubs'),
    path('profile/<str:student_id>/liked-club/', likeClubListView.as_view(), name='liked-club'),
    path('profile/<str:student_id>/scraped-recruit/', recruitScrapListView.as_view(), name='scraped-recruit'),
    ]