import datetime

from django import forms
from django.contrib import admin

from apps.matchmaking.models import League
from common import matchmaking


class LeagueForm(forms.ModelForm):
    start = forms.SplitDateTimeField(required=False)
    end = forms.SplitDateTimeField(required=False)
    active = forms.BooleanField(required=False)
    settings = forms.JSONField(required=False)

    class Meta:
        model = League
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = matchmaking.retrieve_league(instance.pk)
            if initial['end']:
                initial['end'] = datetime.datetime.fromisoformat(initial['end'])
            if initial['start']:
                initial['start'] = datetime.datetime.fromisoformat(initial['start'])
            if 'initial' in kwargs:
                kwargs['initial'].update(initial)
            else:
                kwargs['initial'] = initial

        super().__init__(*args, **kwargs)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    form = LeagueForm

    def save_model(self, request, obj, form, change):
        start = form.cleaned_data.get('start', None)
        end = form.cleaned_data.get('end', None)
        active = form.cleaned_data.get('active', None)
        league_settings = form.cleaned_data.get('settings', None)

        if change:
            matchmaking.update_league(
                league_id=obj.pk,
                start=start,
                end=end,
                active=active,
                league_settings=league_settings,
            )
        else:
            league = matchmaking.create_league(
                start=start,
                end=end,
                active=active,
                league_settings=league_settings,
            )

            obj.id = league['id']

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        matchmaking.delete_league(obj.pk)
        super().delete_model(request, obj)

    def has_delete_permission(self, request, obj=None):
        # TODO: Wait until matchmaking supports deletion
        return False
