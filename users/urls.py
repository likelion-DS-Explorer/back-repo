from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, editPostViewset, UserClubsView, ApplyClubsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:student_id>/', ProfileView.as_view()),
    path('profile/<str:student_id>/edit-posts/', editPostViewset.as_view({'get':'list'}), name='edit_post_list'),
    path('profile/<str:student_id>/affiliated-clubs/', UserClubsView.as_view(), name='affiliated-clubs'),
    path('profile/<str:student_id>/apply/', ApplyClubsView.as_view(), name='apply-clubs'),
    ]