from apps.matchmaking.models import League
from apps.matchmaking.serializers import LeagueSerializer


def get_or_create_league(league_id: int):
    league_name = f'League {league_id}'
    obj, _ = League.objects.get_or_create(id=league_id, defaults={
        'name': league_name,
    })
    return obj


def enrich_league(league: dict):
    league_id = league['id']
    league_obj = get_or_create_league(league_id)

    serializer = LeagueSerializer(instance=league_obj)

    league.update(serializer.data)
