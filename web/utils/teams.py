from apps.teams.models import Team
from apps.teams.serializers import TeamSerializer, TeamShortSerializer


def team_queryset(include_users=False):
    queryset = Team.objects
    if include_users:
        queryset = queryset.prefetch_related(
            'users'
        )

    queryset = queryset.all()
    return queryset


def extend_team(team, include_users=False):
    queryset = team_queryset(include_users)
    team_object = queryset.get(team['id'])

    if include_users:
        serializer_class = TeamSerializer
    else:
        serializer_class = TeamShortSerializer

    serializer = serializer_class(instance=team_object)
    team.update(serializer.data)
