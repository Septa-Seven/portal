from rest_framework import serializers

from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'body',
            'created_at',
            'user',
            'article',
        )
