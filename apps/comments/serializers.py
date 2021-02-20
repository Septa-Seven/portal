from rest_framework import serializers

from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    user_name = serializers.StringRelatedField(source='user')

    class Meta:
        model = Comment
        fields = (
            'id',
            'body',
            'created_at',
            'user',
            'user_name',
            'article',
        )
