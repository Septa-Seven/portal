from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.teams.models import Team


class User(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    team = models.ForeignKey(
        Team,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )

    def __str__(self):
        return self.username
