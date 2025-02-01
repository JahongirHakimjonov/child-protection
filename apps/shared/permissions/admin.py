from rest_framework.permissions import BasePermission

from apps.users.models.users import RoleChoices


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleChoices.ADMIN
