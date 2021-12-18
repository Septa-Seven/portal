from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from django.conf import settings
from utils import matchmaking, teams
from apps.teams.models import Team
from apps.teams.serializers import TeamShortSerializer


def extend_game(game):
    for player in game['players']:
        teams.extend_team(player, include_users=False)


class GamesRetrieveView(APIView):

    def get(self, request, pk, format=None):
        # Handle exceptions
        try:
            game = matchmaking.retrieve_game(pk)
        except ConnectionError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        extend_game(game)
        return Response(game)


class GamesListView(APIView):

    def get(self, request, format=None):
        qp = request.query_params

        try:
            games = matchmaking.list_games(
                qp.get('team_id', None),
                qp.get('league_id', None),
                qp.get('page', 0),
                qp.get('size', None),
            )
        except ConnectionError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        for game in games:
            extend_game(game)

        return Response(games)


@api_view(['GET'])
def retrieve_league(request, pk, format=None):
    user = request.user
    league = matchmaking.retrieve_league(pk)

    attach_connect_url = (user.team is not None)
    if attach_connect_url:
        password = matchmaking.reveal_password(user.id)
        connect_url = matchmaking.construct_connect_url(
            pk, user.id, password
        )
        league['connect_url'] = connect_url

    return Response(league)


@api_view(['GET'])
def league_top(request, pk, format=None):
    league_top = matchmaking.league_top(pk)

    for league_player in league_top:
        teams.extend_team(league_player, include_users=False)

    return Response(league_top)


@api_view(['GET'])
def list_league(request, format=None):
    qp = request.query_params

    leagues = matchmaking.list_leagues(
        qp.get('page', 0),
        qp.get('size', None),
    )
    return Response(leagues)
