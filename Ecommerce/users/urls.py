from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AddressViewSet,
    ProfileAPIView,
    UserAPIView,
    UserRegisterationAPIView,
)

app_name = "users"

router = DefaultRouter()
router.register(r"", AddressViewSet)

urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="user_register"),
    path("", UserAPIView.as_view(), name="user_detail"),
    path("profile/", ProfileAPIView.as_view(), name="profile_detail"),
    path("profile/address/", include(router.urls)),
]
