
def sync_leagues():
    page = 0
    size = 100
    while True:
        leagues = matchmaking.list_leagues(page, size)

        if not leagues:
            break

        for league in leagues:
            save_league(league)


def save_league(league: dict):
    league_id = league['id']
    league_name = f'League {league_id}'
    League.objects.create(id=league_id, name=league_name)
