from rest_framework import permissions, viewsets

from .models import News
from .serializers import NewsDetailSerializer, NewsListSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    # serializer_class = NewsDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            serializer_class = NewsListSerializer
        else:
            serializer_class = NewsDetailSerializer
        return serializer_class

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
