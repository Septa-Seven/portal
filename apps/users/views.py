from django.db.models import Count, When, Case, BooleanField
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import *
from apps.users.permissions import IsLeader, HasNoTeam, IsInvited, IsInviter, IsMember
from apps.users.serializers import TeamSerializer, InvitationSerializer
from septacup_backend.settings import TEAM_SIZE


class TeamViewSet(viewsets.ModelViewSet):
    """
    Вьюсет команды.
    list, retrieve доступен авторизованным пользователям;
    create - авторизованному пользователю без команды;
    update - участнику или лидеру команды;
    delete - лидеру команды или администратору.
    """
    queryset = Team.objects.prefetch_related('users').annotate(members_count=Count('users'))
    serializer_class = TeamSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, HasNoTeam]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update':
            permission_classes = [IsMember]
        else:
            permission_classes = [permissions.IsAdminUser | IsLeader]

        return [permission_class() for permission_class in permission_classes]

    def perform_create(self, serializer):
        serializer.save(leader=self.request.user)

    @action(detail=True, methods=['put'])
    def quit(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.team.leader != user:
            user.team = None
            user.save()
            self.perform_update(serializer)
            return Response(serializer.data)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvitationViewSet(viewsets.ModelViewSet):
    """
    Вьюсет приглашения.
    полный list доступен администратору;
    частичный list доступен адресату и лидеру команды;
    retrieve доступен адресату и лидеру команды;
    create - лидеру команды;
    accept - приглашенному без команды;
    delete - лидеру, приглашенному или администратору.
    """
    team_size = int(TEAM_SIZE)
    queryset = Invitation.objects.prefetch_related('team').annotate(
        count=Count('team__users'),
        active=Case(
            When(count__lt=team_size, then=True),
            When(count__gte=team_size, then=False),
            output_field=BooleanField()
        )
    )
    serializer_class = InvitationSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsLeader]
        elif self.action == 'retrieve':
            permission_classes = [IsInviter | IsInvited]
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser | IsInviter | IsInvited]
        elif self.action == 'accept':
            permission_classes = [IsInvited & HasNoTeam]
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

    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        invitation = self.get_object()
        serializer = self.get_serializer(invitation)

        user = invitation.user
        user.team = invitation.team
        user.save()

        invitation.delete()

        return Response(serializer.data)
