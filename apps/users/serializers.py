from rest_framework import serializers

from apps.users.models import Team, Invitation, User


class TeamSerializer(serializers.ModelSerializer):

    leader = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'leader', 'description',)


class InvitationSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Invitation
        fields = ('id', 'team', 'user',)

    def validate_user(self, user):
        if user.team:
            raise serializers.ValidationError('User already has a team')
        return user
