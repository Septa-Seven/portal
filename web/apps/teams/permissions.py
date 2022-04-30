from rest_framework import permissions


class IsLeader(permissions.BasePermission):
    message = "User is not a leader"

    def has_permission(self, request, view):
        user = request.user

        if user.team:
            return user.team.leader == user

        return False


class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, team):
        return request.user.team == team


class IsInvited(permissions.BasePermission):
    message = "User is not invited"

    def has_object_permission(self, request, view, invitation):
        return invitation.user == request.user


class IsInviter(permissions.BasePermission):
    message = "User is not inviter"

    def has_object_permission(self, request, view, invitation):
        return invitation.team.leader == request.user


class HasTeam(permissions.BasePermission):
    message = "User has no team"

    def has_permission(self, request, view):
        return request.user.team is not None


class HasNoTeam(permissions.BasePermission):
    message = "User has team"

    def has_permission(self, request, view):
        return request.user.team is None
