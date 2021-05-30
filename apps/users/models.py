from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    name = models.CharField(null=False, unique=True, max_length=200)
    description = models.TextField(blank=True)
    leader = models.OneToOneField(
        to='User',
        on_delete=models.CASCADE,
        related_name='leader'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.leader.team = self
        self.leader.is_leader = True
        super(Team, self).save(*args, **kwargs)
        self.leader.save()

    def delete(self, *args, **kwargs):
        self.leader.is_leader = False
        super(Team, self).delete(*args, **kwargs)


class User(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    team = models.ForeignKey(
        Team,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Invitation(models.Model):
    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
