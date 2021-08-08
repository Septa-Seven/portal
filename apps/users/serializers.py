from rest_framework import serializers

from apps.users.models import Team, Invitation, User


class SeptaUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class TeamSerializer(serializers.ModelSerializer):

    leader = serializers.PrimaryKeyRelatedField(read_only=True)
    members_count = serializers.IntegerField(read_only=True)
    users = SeptaUserSerializer(read_only=True, many=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'rating', 'leader', 'members_count', 'users', 'description')


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
