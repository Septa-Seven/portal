import datetime

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import APIException


class MatchmakingException(APIException):
    default_detail = "Matchmaking error"
    default_code = "matchmaking"


def _request(method, url, json=None, params=None):
    response = requests.request(
        method=method,
        url=url,
        params=params,
        json=json,
        headers={'API-Key': settings.MATCHMAKING_API_KEY},
    )
    if 500 <= response.status_code < 600 or response.status_code == 408:
        raise MatchmakingException(
            detail='Matchmaking unavailable',
        )
    return response


def construct_connect_url(league_id: int, user_id: int):
    response = _request(
        method='get',
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}/connect_url/{league_id}',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data['detail'])
    url = data['connect_url']
    return url


def retrieve_user(user_id: int):
    response = _request(
        method='get',
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data['detail'])
    return data


def create_user():
    response = _request(
        method='post',
        url=f'{settings.MATCHMAKING_HTTP}/users/',
    )
    user = response.json()
    return user


def delete_user(user_id: int):
    response = _request(
        method='put',
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data['detail'])
    return data


def user_reset_token(user_id: int):
    response = _request(
        method='put',
        url=f'{settings.MATCHMAKING_HTTP}/users/{user_id}/reset_token',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data['detail'])
    return data


def retrieve_game(game_id: int):
    response = _request(
        method='get',
        url=f'{settings.MATCHMAKING_HTTP}/games/{game_id}',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data['detail'])
    return data


def list_games(user_id: int = None, league_id: int = None, page: int = 0, size: int = None):
    params = {
        'page': page,
    }
    if user_id is not None:
        params['user_id'] = user_id
    if league_id is not None:
        params['league_id'] = league_id
    if size is not None:
        params['size'] = size

    response = _request(
        method='get',
        url=f'{settings.MATCHMAKING_HTTP}/games/',
        params=params,
    )
    games = response.json()
    return games


def retrieve_league(league_id: int):
    response = _request(
        method='get',
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data['detail'])

    return data


def league_top(league_id: int):
    response = _request(
        method='get',
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}/top',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data['detail'])
    return data


def list_leagues(page: int = 0, size: int | None = None):
    params = {
        'page': page,
    }
    if size is not None:
        params['size'] = size

    response = _request(
        method='get',
        url=f'{settings.MATCHMAKING_HTTP}/leagues/',
        params=params,
    )

    leagues = response.json()
    return leagues


def create_league(
    start: datetime.datetime | None = None,
    end: datetime.datetime | None = None,
    active: bool | None = None,
    league_settings: dict | None = None,
):
    data = {
        "settings": league_settings or {},
    }
    if start is not None:
        data['start'] = start.isoformat()
    if end is not None:
        data['end'] = end.isoformat()
    if active is not None:
        data['active'] = active

    response = _request(
        method='post',
        url=f'{settings.MATCHMAKING_HTTP}/leagues/',
        json=data,
    )
    leagues = response.json()
    return leagues


def update_league(
    league_id: int,
    start: datetime.datetime | None = None,
    end: datetime.datetime | None = None,
    active: bool | None = None,
    league_settings: dict | None = None,
):
    data = {
        "settings": league_settings or {},
    }
    if start is not None:
        data['start'] = start.isoformat()
    if end is not None:
        data['end'] = end.isoformat()
    if active is not None:
        data['active'] = active

    response = _request(
        method='put',
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}',
        json=data,
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data['detail'])
    return data


def delete_league(league_id: int):
    response = _request(
        method='delete',
        url=f'{settings.MATCHMAKING_HTTP}/leagues/{league_id}',
    )
    data = response.json()
    if response.status_code == 404:
        raise ValidationError(detail=data['detail'])
    return data
