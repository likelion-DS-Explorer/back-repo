from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, editPostViewset, AddClubMemberView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:student_id>/', ProfileView.as_view()),
    path('profile/<str:student_id>/edit-posts/', editPostViewset.as_view({'get':'list'}), name='edit_post_list'),
    path('profile/<str:student_id>/add-club-member/', AddClubMemberView.as_view(), name="add-club-member")
    ]