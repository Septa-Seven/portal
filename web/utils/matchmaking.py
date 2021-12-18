from django.conf import settings
import requests


def reveal_password(user_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}/reveal_password',
        headers={'API-Key': settings.MATCHMAKING_API_KEY}
    )
    credentials = response.json()
    password = credentials["password"]

    return password


def construct_connect_url(league_id: int, user_id: int, password: str):
    return f"{settings.MATCHMAKING_WS}/connect/{league_id}/{user_id}/{password}"


def retrieve_user(user_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}'
    )
    user = response.json()
    return user


def create_user():
    response = requests.post(
        url=f'{settings.MATCHMAKING_HTTP}/users',
        headers={'API-Key': settings.MATCHMAKING_API_KEY}
    )
    user = response.json()
    return user


def delete_user(user_id: int):
    requests.delete(
        url=f'{settings.MATCHMAKING_HTTP}/players/{user_id}',
        headers={'API-Key': settings.MATCHMAKING_API_KEY}
    )


def user_reset_password(user_id: int):
    requests.put(
        url=f'{settings.MATCHMAKING_HTTP}/players/{user_id}/reset_password',
        headers={'API-Key': settings.MATCHMAKING_API_KEY}
    )


def retrieve_game(game_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/games/{game_id}',
    )
    game = response.json()
    return game


def list_games(user_id: int = None, league_id: int = None, page: int = 0, size: int = None):
    params = {
        'page': page,
    }
    if user_id:
        params['user_id'] = user_id
    if league_id:
        params['league_id'] = league_id
    if size:
        params['size'] = size

    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/games',
        params=params,
    )
    games = response.json()
    return games


def retrieve_league(league_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}',
    )
    league = response.json()
    return league


def league_top(league_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}/top',
    )
    league = response.json()
    return league


def list_leagues(page: int = 0, size: int = None):
    params = {
        'page': page,
        'size': size,
    }
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/leagues',
        params=params,
    )
    leagues = response.json()
    return leagues
