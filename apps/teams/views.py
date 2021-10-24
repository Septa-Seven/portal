from django.db.models import Count, When, Case, BooleanField
from rest_framework import permissions, viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from apps.matchmaking.views import retrieve_team
from apps.teams.models import *
from apps.teams.permissions import IsLeader, HasNoTeam, IsInvited, IsInviter
from apps.teams.serializers import TeamSerializer, InvitationSerializer, TeamShortSerializer
from septacup_backend import settings
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

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'list':
            serializer_class = TeamShortSerializer
        else:
            serializer_class = TeamSerializer
        return serializer_class

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, HasNoTeam]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update':
            permission_classes = [IsLeader]
        else:
            permission_classes = [permissions.IsAdminUser | IsLeader]

        return [permission_class() for permission_class in permission_classes]

    def create(self, request, *args, **kwargs):
        response = requests.post(
            url=f'{settings.MATCHMAKING_URL}/players',
            headers={'API-Key': settings.MATCHMAKING_API_KEY}
        )
        data = response.json()
        data['name'] = request.data['name']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer, data['id'])

        headers = self.get_success_headers(serializer.data)
        data = {'password': data['password'], **serializer.data}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, team_id):
        serializer.save(leader=self.request.user, id=team_id)

    def perform_destroy(self, instance):
        requests.delete(
            url=f'{settings.MATCHMAKING_URL}/players/{instance.id}',
            headers={'API-Key': settings.MATCHMAKING_API_KEY}
        )
        super().perform_destroy(instance)

    @action(detail=True, methods=['put'])
    def reset_password(self, request, *args, **kwargs):
        response = requests.put(
            url=f'{settings.MATCHMAKING_URL}/players/reset_password',
            headers={'API-Key': settings.MATCHMAKING_API_KEY}
        )
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def quit(self, request):
        user = request.user

        if user.team:
            if user.team.leader == user:
                user.team.delete()
            else:
                user.team = None
                user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        response = requests.get(
            url=f'{settings.MATCHMAKING_URL}/players/',
            headers={'API-Key': settings.MATCHMAKING_API_KEY}
        )
        data = response.json()
        for team in data:
            team.update(retrieve_team(team['id']))
        return Response(data, status=status.HTTP_200_OK)


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
