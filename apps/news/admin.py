from django.contrib import admin
from apps.news.models import NewsItem

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'publish',
        'status'
    )
    list_filter = (
        'status',
        'created',
        'publish',
    )
    search_fields = (
        'title',
        'body'
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    date_hierarchy = 'publish'
    ordering = (
        'status',
        'publish'
    )
