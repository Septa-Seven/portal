from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from septacup_backend import settings
from apps.teams.models import Team


def retrieve_team(team_id):
    try:
        team = Team.objects.values('id', 'name').get(pk=team_id)
    except Team.DoesNotExist:
        team = {'id': team_id, 'name': 'deleted'}
    return team


def handle_game(game):
    players = []
    for player in game['players']:
        team = retrieve_team(player['id'])
        players.append(team)

    game['players'] = players
    return game


class GamesRetrieveView(APIView):

    def get(self, request, pk, format=None):
        try:
            response = requests.get(
                url=f'{settings.MATCHMAKING_URL}/games/{pk}',
            )
        except ConnectionError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if response.status_code == 200:
            game = response.json()
            game = handle_game(game)
            return Response(game)

        return Response(status=response.status_code)


class GamesListView(APIView):

    def get(self, request, format=None):

        if 'player_id' in request.query_params:
            params = request.query_params['player_id']
        else:
            params = None
        try:
            response = requests.get(
                url=f'{settings.MATCHMAKING_URL}/games',
                params=params
            )
        except ConnectionError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        games = response.json()
        games = [handle_game(game) for game in games]
        return Response(games)
