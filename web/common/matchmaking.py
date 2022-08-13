import datetime

from django.conf import settings
import requests
from rest_framework.exceptions import ValidationError


class MatchmakingError(Exception):
    def __init__(self, detail, *args):
        self.detail = detail
        super().__init__(*args)


def construct_connect_url(league_id: int, user_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}/connect_url/{league_id}',
        headers={'API-Key': settings.MATCHMAKING_API_KEY}
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data)

    url = data['connect_url']
    return url


def retrieve_user(user_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}'
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data)
    return data


def create_user():
    response = requests.post(
        url=f'{settings.MATCHMAKING_HTTP}/users/',
        headers={'API-Key': settings.MATCHMAKING_API_KEY}
    )
    user = response.json()
    return user


def delete_user(user_id: int):
    response = requests.delete(
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}',
        headers={'API-Key': settings.MATCHMAKING_API_KEY}
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data)
    return data


def user_reset_token(user_id: int):
    response = requests.put(
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}/reset_token',
        headers={'API-Key': settings.MATCHMAKING_API_KEY}
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data)
    return data


def retrieve_game(game_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/games/{game_id}',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data)
    return data


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
        url=f'{settings.MATCHMAKING_HTTP}/games/',
        params=params,
    )
    games = response.json()
    return games


def retrieve_league(league_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data)

    return data


def league_top(league_id: int):
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}/top',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data)
    return data


def list_leagues(page: int = 0, size: int = None):
    params = {
        'page': page,
        'size': size,
    }
    response = requests.get(
        url=f'{settings.MATCHMAKING_HTTP}/leagues/',
        params=params,
    )
    leagues = response.json()
    return leagues


def create_league(start: datetime.datetime, end: datetime.datetime, active: bool):
    data = {
        'start': start.isoformat(),
        'end': end.isoformat(),
        'active': active,
    }
    response = requests.post(
        url=f'{settings.MATCHMAKING_HTTP}/leagues/',
        headers={'API-Key': settings.MATCHMAKING_API_KEY},
        json=data,
    )
    leagues = response.json()
    return leagues


def update_league(league_id: int, start: datetime.datetime, end: datetime.datetime, active: bool):
    data = {
        'start': start.isoformat(),
        'end': end.isoformat(),
        'active': active,
    }
    response = requests.put(
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}',
        headers={'API-Key': settings.MATCHMAKING_API_KEY},
        json=data,
    )
    league = response.json()
    return league


def delete_league(league_id: int):
    response = requests.put(
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}',
        headers={'API-Key': settings.MATCHMAKING_API_KEY},
    )
    league = response.json()
    return league
