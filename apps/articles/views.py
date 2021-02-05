from rest_framework import permissions, viewsets

from apps.articles.models import Article
from apps.articles.serializers import ArticleDetailSerializer, ArticleListSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.filter(status=Article.StatusChoices.PUBLISHED).all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer

        return ArticleDetailSerializer
