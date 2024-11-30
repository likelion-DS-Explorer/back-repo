from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, InquiryViewSet

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:student_id>/', ProfileView.as_view()),
    ]