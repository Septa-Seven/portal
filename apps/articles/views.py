from django.db.models import Count, Prefetch
from django.db.models.expressions import Window
from django.db.models.functions import Lag, Lead

from rest_framework import permissions, viewsets

from apps.articles.models import Article
from apps.articles.serializers import ArticleDetailSerializer, ArticleListSerializer
from apps.comments.models import Comment


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет статьи
    Количество статей в списке на страницу устанавливается в settings.py
    Параметр 'PAGE_SIZE' в REST_FRAMEWORK
    """
    queryset = Article.objects.annotate(
        comments_count=Count('comments'),
        previous_page=Window(expression=Lag('id')),
        next_page=Window(expression=Lead('id'))
    )
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'retrieve':
            queryset = queryset.prefetch_related(
                Prefetch('comments', queryset=Comment.objects.filter(active=True))
            )

        # Admin has access to unpublished articles to visually
        # inspect them after frontend rendering.
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                status=Article.StatusChoices.PUBLISHED
            )

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer

        return ArticleDetailSerializer
