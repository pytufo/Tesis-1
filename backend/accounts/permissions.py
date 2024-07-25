from rest_framework.permissions import BasePermission
from accounts.models import User


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class IsActive(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_active
        )        
