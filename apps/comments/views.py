from rest_framework import permissions, viewsets

from apps.comments.models import Comment
from apps.comments.serializers import CommentListSerializer, CommentDetailSerializer
from apps.comments.permissions import IsOwner


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет комментария.
    list, retrieve доступен всем (даже неавторизованным);
    create - авторзованному пользователю;
    delete - владельцу комментария.
    """
    queryset = Comment.objects.filter(active=True).all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer

        return CommentDetailSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser, IsOwner]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission_class() for permission_class in permission_classes]
