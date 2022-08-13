from django.db.models import Count

from apps.teams.models import Team
from apps.teams.serializers import TeamSerializer, TeamShortSerializer


def team_queryset(include_users=False):
    queryset = Team.objects
    if include_users:
        queryset = queryset.prefetch_related(
            'users'
        ).annotate(
            members_count=Count('users')
        )

    queryset = queryset.all()
    return queryset


def extend_team(team, include_users=False):
    queryset = team_queryset(include_users)
    try:
        team_object = queryset.get(pk=team['id'])
    except Team.DoesNotExist:
        extend_info = {
            'name': 'Not found',
            'description': None,
        }
    else:
        if include_users:
            serializer_class = TeamSerializer
        else:
            serializer_class = TeamShortSerializer

        serializer = serializer_class(instance=team_object)
        extend_info = serializer.data

    team.update(extend_info)
