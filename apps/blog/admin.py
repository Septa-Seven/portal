from django.contrib import admin
from apps.blog.models import Article, Comment


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'article',
        'active',
    )
    list_filter = (
        'active',
        'created_at',
    )
    search_fields = (
        'body',
        'article',
        'user',
    )
    date_hierarchy = 'created_at'
    ordering = (
        'active',
        'article',
        'user',
    )
