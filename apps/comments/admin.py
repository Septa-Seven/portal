from django.contrib import admin
from apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'news',
        'publish',
        'active'
    )
    list_filter = (
        'active',
        'created',
        'publish',
    )
    search_fields = (
        'body',
        'news',
        'user'
    )
    date_hierarchy = 'publish'
    ordering = (
        'active',
        'publish',
        'news',
        'user'
    )