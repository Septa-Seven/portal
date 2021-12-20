from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.teams.permissions import HasTeam
from apps.users.models import User
from apps.users.serializers import UserSerializer, UserListSerializer


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = self.queryset.only('id', 'username')

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            serializer_class = UserListSerializer
        else:
            serializer_class = UserSerializer

        return serializer_class

    def filter_queryset(self, queryset):
        if self.action == 'list':
            username = self.request.query_params.get('username')

            if username is not None:
                queryset = queryset.filter(username__contains=username)

        return queryset
