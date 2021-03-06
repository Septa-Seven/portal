from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, filters
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.strategies.permissions import IsOwner
from apps.strategies.tasks import build_strategy_image_task
from apps.strategies.models import Strategy
from apps.strategies.serializers import StrategySerializer


class StrategyViewSet(ModelViewSet):
    """
    Вьюсет стратегии.
    create -  доступен авторизованному пользователю;
    delete - администратору или владельцу стратегии;
    (partial) update - владельцу стратегии.
    возможен фильтр списка стратегий по пользователю
    """
    serializer_class = StrategySerializer
    queryset = Strategy.objects.all()

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['user_id']

    def get_queryset(self):
        queryset = Strategy.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user=user_id)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser | IsOwner]
        else:
            permission_classes = [IsOwner]

        return [permission_class() for permission_class in permission_classes]

    def create(self, request, *args, **kwargs):
        # TODO: уточнить контент-тип,
        #  возможно вместо строк 42-43 использовать 40-41
        content = request.data['file']
        # content_type = content.content_type
        # if content_type in settings.CONTENT_TYPES:
        file_ext = content.name.split('.')[-1]
        if file_ext == 'zip':
            if content.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)))
        else:
            raise ValidationError(_('File type is not supported'))

        strategy = super().create(request, *args, **kwargs)
        # build_strategy_image_task.delay(strategy.id)
        return strategy

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # TODO: удаление файла и докер образа
        super().destroy(request, *args, **kwargs)
