from rest_framework import filters


class UsersWithoutTeamFilter(filters.BaseFilterBackend):
    """
    Return all objects which match any of the provided tags
    """

    def filter_queryset(self, request, queryset, view):
        user = request.query_params.get('user', None)
        queryset = queryset.filter(tags__name__in=tags).distinct()

        return queryset
