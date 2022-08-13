from apps.matchmaking.models import League
from apps.matchmaking.serializers import LeagueSerializer


def extend_league(league: dict):
    league_id = league['id']
    try:
        league_obj = League.objects.get(pk=league_id)
    except League.DoesNotExist:
        league_extra = {
            "name": f"League {league_id}",
            "description": None,
        }
    else:
        serializer = LeagueSerializer(instance=league_obj)
        league_extra = serializer.data

    league.update(league_extra)
