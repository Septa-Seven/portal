from rest_framework import serializers

from apps.teams.models import Team, Invitation
from apps.users.serializer import UserSerializier
from django.conf import settings


class TeamSerializer(serializers.ModelSerializer):

    leader = serializers.PrimaryKeyRelatedField(read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    users = UserSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'rating',
            'leader',
            'members_count',
            'description',
            'users',
        )


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
