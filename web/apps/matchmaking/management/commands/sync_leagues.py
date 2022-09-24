from django.core.management.base import BaseCommand

from common import matchmaking
from common.leagues import get_or_create_league


class Command(BaseCommand):
    help = 'Sync leagues'

    def handle(self, *args, **options):
        page = 0
        size = 100
        while True:
            leagues = matchmaking.list_leagues(page, size)

            if not leagues:
                break

            for league in leagues:
                get_or_create_league(league['id'])
