from celery import shared_task

from apps.strategies.building import build_strategy_image


@shared_task
def build_strategy_image_task(strategy_id):
    build_strategy_image(strategy_id)
