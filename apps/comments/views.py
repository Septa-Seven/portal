from rest_framework import permissions, viewsets

from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.comments.permissions import IsOwner


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет комментария.
    list, retrieve доступен всем (даже неавторизованным);
    create - авторизованному пользователю;
    delete - владельцу комментария.
    """
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser | IsOwner]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission_class() for permission_class in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
