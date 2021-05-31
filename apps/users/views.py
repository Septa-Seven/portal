from rest_framework import permissions, viewsets

from apps.users.models import *
from apps.users.permissions import IsLeader, HasNoTeam, IsInvited, IsInviter
from apps.users.serializers import TeamSerializer, InvitationSerializer


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
        serializer.save(leader=self.request.user)


class InvitationViewSet(viewsets.ModelViewSet):
    """
    Вьюсет приглашения.
    полный list доступен администратору;
    частичный list доступен адресату и лидеру команды;
    retrieve доступен адресату и лидеру команды;
    create, delete - лидеру команды.
    """

    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsLeader]
        elif self.action == 'retrieve':
            permission_classes = [IsInviter | IsInvited]
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser | IsInviter]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission_class() for permission_class in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(team=self.request.user.team)
