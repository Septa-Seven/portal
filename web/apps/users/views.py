from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from apps.users.models import User
from apps.users.serializer import UserSerializer


class UserListView(ListModelMixin, GenericAPIView):
    queryset = User.objects.only('id', 'username')
    serializer_class = UserSerializer

    def filter_queryset(self, queryset):
        username = self.request.query_params.get('username')

        if username is not None:
            queryset = queryset.filter(username__contains=username)

        return queryset
