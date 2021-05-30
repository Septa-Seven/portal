from django.contrib import admin
from apps.users.models import *

admin.site.register(Invitation)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'team'
    )
    list_filter = (
        'team',
        'username',
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'leader',
    )
    list_filter = (
        'name',
        'leader',
    )
