from rest_framework import permissions, viewsets

from apps.comments.models import Comment
from apps.comments.serializers import CommentListSerializer, CommentDetailSerializer
from apps.comments.permissions import IsOwner


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет комментария.
    list, retrieve доступен всем (даже неавторизованным);
    create - авторзованному пользователю,
    delete - владельцу комментария.
    """
    queryset = Comment.objects.filter(active=True).all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer

        return CommentDetailSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'delete':
            self.permission_classes = [permissions.IsAdminUser, IsOwner]
        return super(self.__class__, self).get_permissions()
