from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Damos permisos (GET, HEAD, OPTIONS) a todos los usuarios ( o no logueados)

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_superuser
