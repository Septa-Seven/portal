from rest_framework import permissions, viewsets

from apps.news.models import News
from apps.news.serializers import NewsPreviewSerializer, NewsFullSerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(status=News.StatusChoices.PUBLISHED).all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            serializer_class = NewsPreviewSerializer
        else:
            serializer_class = NewsFullSerializer

        return serializer_class
