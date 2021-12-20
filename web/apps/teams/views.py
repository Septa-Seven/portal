from django.db.models import Count, When, Case, BooleanField
from rest_framework import permissions, viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from utils import matchmaking, teams
from apps.teams.models import *
from apps.teams.permissions import IsLeader, HasTeam, IsInvited, IsInviter
from apps.teams.serializers import (
    TeamSerializer,
    InvitationSerializer,
    TeamShortSerializer,
)
from django.conf import settings


class TeamViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Team.objects.prefetch_related(
        'users'
    ).annotate(
        members_count=Count('users')
    )

    def get_queryset(self):
        if self.action == 'retrieve':
            queryset = teams.team_queryset(include_users=True)
        else:
            queryset = teams.team_queryset()

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            serializer_class = TeamShortSerializer
        else:
            serializer_class = TeamSerializer

        return serializer_class

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, ~HasTeam]
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
        # TODO: Handle requests exception
        team = matchmaking.create_user()
        team['name'] = request.data['name']

        serializer = self.get_serializer(data=team)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer, team['id'])

        headers = self.get_success_headers(serializer.data)
        data = {
            'password': team['password'],
            **serializer.data
        }

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        team = self.get_object()

        attach_connect_url = (request.user.team == team)

        # TODO: Handle requests exception
        team_data = matchmaking.retrieve_user(team.id)

        serializer = self.get_serializer(team)
        team_data.update(serializer.data)

        if attach_connect_url:
            password = matchmaking.reveal_password(team.id)

            for league_player in team_data["league_players"]:
                league_id = league_player["league"]["id"]
                connect_url = matchmaking.construct_connect_url(
                    league_id, team.id, password
                )
                league_player["connect_url"] = connect_url

        return Response(team_data, status=status.HTTP_200_OK)

    def perform_create(self, serializer, team_id):
        serializer.save(leader=self.request.user, id=team_id)

    def perform_destroy(self, instance):
        # TODO: Handle requests exception
        matchmaking.delete_user(instance.id)
        super().perform_destroy(instance)

    @action(detail=True, methods=['put'], permission_classes=[IsLeader])
    def reset_password(self, request, pk):
        # TODO: Handle requests exception
        credentials = matchmaking.user_reset_password(pk)
        return Response(credentials, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['put'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def quit(self, request):
        user = request.user

        if user.team:
            if user.team.leader == user:
                self.perform_destroy(user.team)
            else:
                user.team = None
                user.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='settings')
    def team_settings(self, request):
        return Response({"max_team_size": settings.TEAM_SIZE})

    @action(detail=False, methods=['GET'], permission_classes=[HasTeam])
    def my(self, request):
        self.kwargs['pk'] = self.request.user.team.pk
        return self.retrieve(request)


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
    queryset = Invitation.objects.prefetch_related('team').annotate(
        count=Count('team__users'),
        active=Case(
            When(count__lt=settings.TEAM_SIZE, then=True),
            When(count__gte=settings.TEAM_SIZE, then=False),
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
            permission_classes = [IsInvited & (~HasTeam)]
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
        serializer.is_valid(raise_exception=True)

        user = invitation.user
        user.team = invitation.team
        user.save()

        invitation.delete()

        return Response(serializer.data)
