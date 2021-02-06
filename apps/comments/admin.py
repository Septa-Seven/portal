from django.contrib import admin
from apps.comments.models import Comment


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
