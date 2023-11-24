from rest_framework.permissions import BasePermission


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_active and request.user.is_active:
            return request.user.is_superuser or request.method in ["GET"]
        return False
