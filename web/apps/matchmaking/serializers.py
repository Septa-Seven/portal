from rest_framework.serializers import ModelSerializer

from apps.matchmaking.models import League


class LeagueSerializer(ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'
