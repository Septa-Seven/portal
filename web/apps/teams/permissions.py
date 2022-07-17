from rest_framework import permissions


class IsLeader(permissions.BasePermission):
    message = "User is not a leader"

    def has_permission(self, request, view):
        user = request.user
        return not user.is_anonymous and user.team and user.team.leader == user


class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, team):
        user = request.user
        return not user.is_anonymous and user.team == team


class IsInvited(permissions.BasePermission):
    message = "User is not invited"

    def has_object_permission(self, request, view, invitation):
        return invitation.user == request.user


class IsInviter(permissions.BasePermission):
    message = "User is not inviter"

    def has_object_permission(self, request, view, invitation):
        return not request.user.is_anonymous and invitation.team.leader == request.user


class HasTeam(permissions.BasePermission):
    message = "User has no team"

    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.team is not None


class HasNoTeam(permissions.BasePermission):
    message = "User has team"

    def has_permission(self, request, view):
        user = request.user
        return user.is_anonymous or user.team is None
