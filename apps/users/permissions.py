from rest_framework import permissions


class IsLeader(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.team:
            return user.team.leader == user

        return False


class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.team == obj


class IsInvited(permissions.BasePermission):
    def has_object_permission(self, request, view, invitation):
        return invitation.user == request.user


class IsInviter(permissions.BasePermission):
    def has_object_permission(self, request, view, invitation):
        return invitation.team.leader == request.user


class HasNoTeam(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.user.team
