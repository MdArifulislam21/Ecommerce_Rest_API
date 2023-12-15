from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import permissions, status
from rest_framework.generics import (
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
)
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.models import UserAddress, Profile
from users.permissions import IsAddressOwner, IsProfileOwner
from users.serializers import (
    AddressReadOnlySerializer,
    ProfileSerializer,
    UserRegistrationSerializer,
    UserSerializer
)

User = get_user_model()


class UserRegisterationAPIView(CreateAPIView):
    """
    Create a user with email and password.
    """

    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = ""
        response_data = {"detail": _("User created.")}
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)




class ProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsProfileOwner,)

    def get_object(self):
        try:
            return self.request.user.profile
        except:
            return Profile.objects.get_or_create(user=self.request.user)


class UserAPIView(RetrieveAPIView):
    """
    Get user details
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AddressViewSet(ReadOnlyModelViewSet):
    """
    List and Retrieve user addresses
    """

    queryset = UserAddress.objects.all()
    serializer_class = AddressReadOnlySerializer
    permission_classes = (IsAddressOwner,)

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(user=user)
