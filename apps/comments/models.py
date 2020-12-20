from django.db import models
from django.utils import timezone

from ..news.models import News
from ..users.models import User


class Comment(models.Model):
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # to hide some unacceptable comments
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f'Comment by {self.user} on {self.news}'
