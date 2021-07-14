from rest_framework import permissions


class IsLeader(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.team:
            return user.team.leader == user

        return False


class IsInvited(permissions.BasePermission):
    def has_object_permission(self, request, view, invitation):
        print('this print from permission')
        print(invitation.user)
        print(request.user)
        return invitation.user == request.user


class IsInviter(permissions.BasePermission):
    def has_object_permission(self, request, view, invitation):
        return invitation.team.leader == request.user


class HasNoTeam(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.user.team
