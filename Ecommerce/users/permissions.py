from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """
    Check if authenticated user is owner of the profile, if not return false
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class IsAddressOwner(BasePermission):
    """
    Check if authenticated user is owner of the address, if not return false
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
