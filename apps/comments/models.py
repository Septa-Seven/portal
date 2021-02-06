from django.db import models

from apps.articles.models import Article
from apps.users.models import User


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Comment(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # to hide some unacceptable comments
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    active_objects = ActiveManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment by {self.user} on {self.article}'
