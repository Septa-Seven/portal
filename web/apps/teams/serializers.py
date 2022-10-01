from rest_framework import serializers

from apps.teams.models import Team, Invitation
from apps.users.serializers import UserPreviewSerializer


class TeamSerializer(serializers.ModelSerializer):

    leader = serializers.PrimaryKeyRelatedField(read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    users = UserPreviewSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'leader',
            'members_count',
            'description',
            'users',
        )


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'description')


class TeamShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name')


class ExpelUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class CurrentUsersTeamDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.team

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class CreateInvitationSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(read_only=True)
    team = TeamShortSerializer(
        default=CurrentUsersTeamDefault(),
    )

    class Meta:
        model = Invitation
        fields = ('id', 'user', 'team', 'active')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Invitation.objects.all(),
                fields=['user', 'team'],
            )
        ]

    def validate_user(self, user):
        if user.team:
            raise serializers.ValidationError('User already has a team')
        return user


class InvitationSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(read_only=True)
    user_name = serializers.SlugRelatedField(
        source='user',
        slug_field='username',
        read_only=True,
    )
    team_name = serializers.SlugRelatedField(
        source='team',
        slug_field='name',
        read_only=True,
     )

    class Meta:
        model = Invitation
        fields = ('id', 'user', 'user_name', 'team', 'team_name', 'active')
