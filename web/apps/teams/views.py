from rest_framework import permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from apps.teams.services import querysets
from utils import matchmaking, teams
from apps.teams.models import *
from apps.teams.permissions import IsLeader, HasTeam, HasNoTeam, IsInvited, IsInviter
from apps.teams.serializers import (
    CreateInvitationSerializer,
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

    def get_queryset(self):
        if self.action == 'retrieve':
            queryset = teams.team_queryset(include_users=True)
        else:
            queryset = teams.team_queryset()

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            serializer_class = TeamShortSerializer
        elif self.action == 'invitations':
            serializer_class = InvitationSerializer
        else:
            serializer_class = TeamSerializer

        return serializer_class

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, HasNoTeam]
        elif self.action == 'retrieve':
            permission_classes = []
        elif self.action == 'update':
            permission_classes = [permissions.IsAuthenticated, IsLeader]
        elif self.action == 'my':
            permission_classes = [permissions.IsAuthenticated, HasTeam]
        elif self.action == 'quit':
            permission_classes = [permissions.IsAuthenticated, HasTeam]
        elif self.action == 'reset_token':
            permission_classes = [permissions.IsAuthenticated, IsLeader]
        else:
            permission_classes = [permissions.IsAdminUser | IsLeader]

        return [permission_class() for permission_class in permission_classes]

    def create(self, request, *args, **kwargs):
        # TODO: Handle requests exception
        team = matchmaking.create_user()
        # TODO: name always must be provided
        team['name'] = request.data['name']

        serializer = self.get_serializer(data=team)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer, team['id'])

        headers = self.get_success_headers(serializer.data)
        data = {
            **serializer.data
        }

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        team = self.get_object()

        attach_connect_url = (not request.user.is_anonymous and request.user.team == team)

        # TODO: Handle requests exception
        team_data = matchmaking.retrieve_user(team.id)

        serializer = self.get_serializer(team)
        team_data.update(serializer.data)

        if attach_connect_url:
            for league_player in team_data["league_players"]:
                league_id = league_player["league"]["id"]
                connect_url = matchmaking.construct_connect_url(
                    league_id, team.id
                )
                league_player["connect_url"] = connect_url

        return Response(team_data, status=status.HTTP_200_OK)

    def perform_create(self, serializer, team_id):
        serializer.save(leader=self.request.user, id=team_id)

    def perform_destroy(self, instance):
        # TODO: Handle requests exception
        matchmaking.delete_user(instance.id)
        super().perform_destroy(instance)

    @action(detail=True, methods=['POST'])
    def reset_token(self, request, pk):
        # TODO: Handle requests exception
        credentials = matchmaking.user_reset_token(pk)
        return Response(credentials, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def quit(self, request):
        user = request.user

        if user.team:
            if user.team.leader == user:
                self.perform_destroy(user.team)
            else:
                user.team = None
                user.save()

            return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='settings')
    def team_settings(self, request):
        return Response({"max_team_size": settings.TEAM_SIZE})

    @action(detail=False, methods=['GET'])
    def my(self, request):
        team = self.request.user.team
        self.kwargs['pk'] = team.pk if team else None
        return self.retrieve(request)


class InvitationViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """
    Вьюсет приглашения.
    полный list доступен администратору;
    частичный list доступен адресату и лидеру команды;
    retrieve доступен адресату и лидеру команды;
    create - лидеру команды;
    accept - приглашенному без команды;
    delete - лидеру, приглашенному или администратору.
    """
    queryset = querysets.invitations_queryset()

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]

        if self.action == 'create':
            permission_classes += [IsLeader]
        elif self.action == 'retrieve':
            permission_classes += [IsInviter | IsInvited]
        elif self.action == 'delete':
            permission_classes += [permissions.IsAdminUser | IsInviter | IsInvited]
        elif self.action == 'accept':
            permission_classes += [HasNoTeam, IsInvited]
        elif self.action == 'list':
            permission_classes += [HasTeam, IsLeader]

        return [permission_class() for permission_class in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(team=self.request.user.team)

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            serializer_class = CreateInvitationSerializer
        else:
            serializer_class = InvitationSerializer

        return serializer_class

    @action(detail=True, methods=['POST'])
    def accept(self, request, *args, **kwargs):
        invitation = self.get_object()

        user = invitation.user
        user.team = invitation.team
        user.save()

        invitation.delete()

        return Response(status=status.HTTP_200_OK)