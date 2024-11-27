from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = "recruit"

default_router = routers.SimpleRouter()
default_router.register("club-recruit", ClubRecruitViewSet)

urlpatterns = [
    path("", include(default_router.urls)),
]