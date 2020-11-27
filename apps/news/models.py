from django.db import models
from django.utils import timezone
from django_editorjs_fields import EditorJsJSONField


class News(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = ('draft', 'Draft')
        PUBLISHED = ('published', 'Published')

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    body = EditorJsJSONField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
