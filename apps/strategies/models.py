from django.db import models
from apps.users.models import User


class ProgrammingLanguage(models.Model):

    name = models.CharField(
        max_length=256,
        unique=True,
    )

    active = models.BooleanField(
        default=True,
    )


class Strategy(models.Model):

    # TODO: добавить сигнал на очистку данных при удалении
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    compiled = models.BooleanField(
        default=False,
    )

    programming_language = models.ForeignKey(
        ProgrammingLanguage,
        on_delete=models.PROTECT,
    )

    # TODO: Определить формат наименований файлов стратегий
    file = models.FileField(
        upload_to='strategies/',
    )
