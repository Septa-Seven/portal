from rest_framework import permissions, viewsets

from apps.users.filters import UsersWithoutTeamFilter
from apps.users.models import *
from apps.users.permissions import IsLeader, HasNoTeam, IsInvited
from apps.users.serializers import UserSerializer, TeamSerializer, InvitationSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
    Вьюсет команды.
    list, retrieve доступен авторизованным пользователям;
    create - авторизованному пользователю без команды;
    delete - лидеру команды или администратору.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, HasNoTeam]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser | IsLeader]

        return [permission_class() for permission_class in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# TODO ?permissions ?qs filter
class InvitationViewSet(viewsets.ModelViewSet):
    """
    Вьюсет приглашения.
    полный list доступен администратору;
    частичный list доступен адресату и лидеру команды;
    retrieve доступен адресату и лидеру команды;
    create, delete - лидеру команды.
    """
    filter_backends = (UsersWithoutTeamFilter,)
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsLeader]
        elif self.action == 'retrieve':
            permission_classes = [IsLeader | IsInvited]
        elif self.action == 'list':
            permission_classes = [permissions.IsAdminUser | IsInvited]
        else:
            permission_classes = [permissions.IsAdminUser | IsLeader]

        return [permission_class() for permission_class in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
