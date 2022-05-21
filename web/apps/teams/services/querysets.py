from django.db.models import Count, When, Case, BooleanField

from apps.teams.models import Invitation
from portal import settings


def invitations_queryset():
    return Invitation.objects.prefetch_related('team').annotate(
        count=Count('team__users'),
        active=Case(
            When(count__lt=settings.TEAM_SIZE, then=True),
            When(count__gte=settings.TEAM_SIZE, then=False),
            output_field=BooleanField()
        )
    )
