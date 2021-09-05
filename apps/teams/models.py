from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True, editable=False)
    name = models.CharField(null=False, unique=True, max_length=200)
    description = models.TextField(blank=True)
    rating = models.FloatField(null=False, default=0)
    leader = models.OneToOneField(
        to='User',
        on_delete=models.CASCADE,
        related_name='leading_team'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.leader.team = self
        super().save(*args, **kwargs)
        self.leader.save()


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


class Invitation(models.Model):
    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
        related_name='invitations',
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='invitations',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'user'], name='unique invitation')
        ]
