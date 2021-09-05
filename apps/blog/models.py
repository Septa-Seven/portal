from django.db import models
from django_editorjs_fields import EditorJsJSONField
from taggit.managers import TaggableManager

from apps.teams.models import User


class Article(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = ('draft', 'Draft')
        PUBLISHED = ('published', 'Published')

    title = models.CharField(max_length=250)

    body = EditorJsJSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=9,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )

    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ('-created_at',)

    def get_tags_display(self):
        return self.tags.values_list('name', flat=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)  # to hide some unacceptable comments

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='article_comments'
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment by {self.user} on {self.article}'
