from django.db import models
from django_editorjs_fields import EditorJsJSONField


class Article(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = ('draft', 'Draft')
        PUBLISHED = ('published', 'Published')

    title = models.CharField(max_length=250)
    body = EditorJsJSONField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
