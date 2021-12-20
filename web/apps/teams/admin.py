from django.contrib import admin
from apps.teams.models import *


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'leader',
    )
    list_filter = (
        'id',
        'name',
        'leader',
    )


@admin.register(Invitation)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'team',
        'user',
    )
    list_filter = (
        'id',
        'team',
        'user',
    )
