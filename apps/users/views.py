from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
            print(self.action)
            permission_classes = [IsLeader]
        elif self.action == 'retrieve':
            permission_classes = [IsInviter | IsInvited]
            print(self.action)
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser | IsInviter]
        elif self.action == 'accept':
            permission_classes = [IsInvited | HasNoTeam]
        elif self.action == 'decline':
            permission_classes = [IsInvited]
        else:
            permission_classes = [permissions.IsAuthenticated]
            print(self.action)
            print(permission_classes)

        return [permission_class() for permission_class in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(team=self.request.user.team)

    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        instance = self.get_object()
        print('this print from view action accept')
        serializer = self.get_serializer(instance)
        print('serializer data', serializer.data)
        user = User.objects.get(id=serializer.data['user'])
        team = Team.objects.get(id=serializer.data['team'])
        user.team = team
        user.save()
        invitation = Invitation.objects.get(id=serializer.data['id'])
        invitation.delete()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        instance = self.get_object()
        print('this print from view action decline')
        serializer = self.get_serializer(instance)
        print('serializer data', serializer.data)
        invitation = Invitation.objects.get(id=serializer.data['id'])
        invitation.delete()
        return Response(serializer.data)
