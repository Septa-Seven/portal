import requests
from rest_framework import serializers

from apps.teams.models import Team, Invitation


class TeamSerializer(serializers.ModelSerializer):

    leader = serializers.PrimaryKeyRelatedField(read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'rating', 'leader', 'members_count', 'description')


class TeamShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name')


class InvitationSerializer(serializers.ModelSerializer):
    team = TeamShortSerializer(read_only=True)
    active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Invitation
        fields = ('id', 'team', 'user', 'active')

    def validate_user(self, user):
        if user.team:
            raise serializers.ValidationError('User already has a team')
        return user
