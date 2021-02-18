import os
import zipfile
import tempfile

import docker

from apps.strategies.models import Strategy
from django.conf import settings


class StrategyBuildFailed(Exception):
    pass


def build_image(client, dockerfile_path, image_tag):
    try:
        client.images.build(path=dockerfile_path, tag=image_tag)
    except docker.errors.BuildError:
        # TODO: подробное описание ошибки почему не забилдилось
        raise StrategyBuildFailed()

    client.images.push(settings.REGISTRY_REPOSITORY, tag=image_tag)


def get_strategy(strategy_id: int) -> Strategy:
    try:
        return Strategy.objects.select_related(
            'programming_language', 'user'
        ).only(
            'programming_language__name',
            'user_id',
            'file',
            'compiled',
        ).get(
            pk=strategy_id, compiled=False
        )
    except Strategy.DoesNotExist:
        raise StrategyBuildFailed(f'Strategy is already compiled or there is no strategy with id {strategy_id}.')


def validate_image_does_not_exist(client, image_tag):
    image_name = settings.STRATEGY_IMAGE_NAME_FORMAT.format(
        repository=settings.REGISTRY_REPOSITORY,
        tag=image_tag
    )

    try:
        image_registry_data = client.images.get_registry_data(image_name)
    except docker.errors.APIError:
        pass
    else:
        raise StrategyBuildFailed(f'Image already exists: {image_name}')


def build_strategy_image(strategy_id: int):
    strategy = get_strategy(strategy_id)

    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(strategy.file, 'rb') as strategy_zip:
            strategy_zip.extractall(temp_dir.name)

        build_environment = {
            'DOCKER_HOST': os.environ['DOCKER_HOST'],
            'STRATEGY_PATH': temp_dir.name,
        }

        client = docker.from_env(environment=build_environment)

        image_tag = settings.STRATEGY_IMAGE_TAG_FORMAT.format(
            user_id=strategy.user_id,
            programming_language=strategy.programming_language.name,
            strategy_id=strategy.id,
        )

        validate_image_does_not_exist(client, image_tag)

        dockerfile_path = os.path.join(__file__, 'dockerfiles', strategy.programming_language.name)
        build_image(client, dockerfile_path, image_tag)

        strategy.compiled = True
        strategy.save()

        client.images.prune()
