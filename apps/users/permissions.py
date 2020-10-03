from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, user):
        if request.method in SAFE_METHODS:
            return True
        return user == request.user
