from rest_framework import serializers

from .models import Article

from apps.comments.serializers import CommentSerializer


class ArticleListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'body',
            'created_at',
            'updated_at',
            'comments_count',
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'body',
            'created_at',
            'updated_at',
            'comments_count',
            'comments',
        )
