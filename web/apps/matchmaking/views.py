from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common import matchmaking, teams, leagues


def extend_game(game):
    for player in game['players']:
        teams.enrich_team(player, include_users=False)


class GamesRetrieveView(APIView):

    def get(self, request, pk, format=None):
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


class LeagueRetrieveView(APIView):

    def get(self, request, pk, format=None):
        user = request.user
        league = matchmaking.retrieve_league(pk)

        attach_connect_url = (hasattr(user, 'team') and user.team is not None)
        if attach_connect_url:
            connect_url = matchmaking.construct_connect_url(
                pk,
                user.team.id,
            )
            league['connect_url'] = connect_url

        leagues.enrich_league(league)

        return Response(league)


class LeagueTopView(APIView):

    def get(self, request, pk, format=None):
        league_top = matchmaking.league_top(pk)

        for league_player in league_top:
            teams.enrich_team(league_player, include_users=False)

        return Response(league_top)


class LeagueListView(APIView):

    def get(self, request, format=None):
        qp = request.query_params

        leagues_ = matchmaking.list_leagues(
            qp.get('page', 0),
            qp.get('size'),
        )

        for league in leagues_:
            leagues.enrich_league(league)

        return Response(leagues_)
