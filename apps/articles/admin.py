from django.contrib import admin
from apps.articles.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'status'
    )
    list_filter = (
        'status',
        'created_at',
    )
    search_fields = (
        'title',
        'body'
    )
    ordering = (
        'status',
    )
