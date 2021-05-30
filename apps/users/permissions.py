from rest_framework import permissions


class IsLeader(permissions.BasePermission):
    """
    Object-level permission to only allow team leaders if they're owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    Here for invitations it's 'user'
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_leader:
            return obj.user == request.user
        return False


class IsInvited(permissions.BasePermission):  # not sure if it's correct
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class HasNoTeam(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.team:
            return False
        return True
