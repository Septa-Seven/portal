from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, permissions
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.teams.models import Invitation
from apps.teams.permissions import IsLeader
from apps.teams.serializers import InvitationSerializer
from apps.teams.services import querysets
from apps.users.models import User
from apps.users.serializers import UserSerializer, UserPreviewSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.only('id', 'username')

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            serializer_class = UserPreviewSerializer
        else:
            serializer_class = UserSerializer

        return serializer_class

    def filter_queryset(self, queryset):
        if self.action == 'list':
            username = self.request.query_params.get('username')
            has_team = self.request.query_params.get('has_team')

            if username is not None:
                queryset = queryset.filter(username__contains=username)

            if has_team is not None:
                if has_team == "1":
                    queryset = queryset.exclude(team__isnull=True)
                else:
                    queryset = queryset.filter(team__isnull=True)

            is_leader = IsLeader().has_permission(self.request, self)
            if is_leader:
                users_with_invitation = Invitation.objects.filter(
                    team=self.request.user.team
                ).values("user_id")
                queryset = queryset.exclude(id__in=users_with_invitation)

        return queryset

    @method_decorator(cache_page(60 * 5))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class UserInvitationsListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = querysets.invitations_queryset()
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
