from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from apps.strategies.tasks import build_strategy_image_task
from apps.strategies.models import Strategy
from apps.strategies.serializers import StrategySerializer


class StrategyViewSet(ModelViewSet):
    serializer_class = StrategySerializer
    queryset = Strategy.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['user_id']

    def create(self, request, *args, **kwargs):
        # TODO: валидация файла
        strategy = super().create(request, *args, **kwargs)
        build_strategy_image_task.delay(strategy.id)
        return strategy

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # TODO: удаление файла и докер образа
        super().destroy(request, *args, **kwargs)
