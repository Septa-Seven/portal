from django.db.models import Count, Prefetch, Subquery
from django.db.models.expressions import OuterRef

from rest_framework import permissions, viewsets, mixins

from apps.blog.filters import TagsFilter
from apps.blog.serializers import *
from apps.blog.permissions import IsOwner


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    Вьюсет комментария.
    list, retrieve отдельно нет, комменты только под статьями;
    create -  доступен авторизованному пользователю;
    delete -  доступен админу или владельцу комментария.
    """
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser | IsOwner]

        # TODO: permission_classes referenced before assignment on GET
        #  but get must be 404 before get_permissions

        return [permission_class() for permission_class in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет статьи
    возможно передать в параметрах значение тега для фильтра статей
    при нескольких значениях для фильтра - в формате или-или
    """
    filter_backends = (TagsFilter,)
    search_fields = ('tags__name',)

    queryset = Article.objects.annotate(
        comments_count=Count('article_comments')
    ).order_by('-created_at')
    permission_classes = (permissions.AllowAny,)

    # def get_similar_articles(self):
    #     similar_articles = self.get_object().tags.similar_objects()
    #     return similar_articles
    #
    # similar_articles = get_similar_articles(self)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'retrieve':
            queryset = queryset.annotate(
                previous_article_id=Subquery(
                    queryset=Article.objects.filter(
                        created_at__lt=OuterRef('created_at')
                    ).order_by('-created_at').values('id')[:1]
                ),
                next_article_id=Subquery(
                    queryset=Article.objects.filter(
                        created_at__gt=OuterRef('created_at')
                    ).order_by('created_at').values('id')[:1]
                )
            ).prefetch_related(
                Prefetch('article_comments', queryset=Comment.objects.filter(active=True))
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
