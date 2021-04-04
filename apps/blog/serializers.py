from rest_framework import serializers

from .models import Article, Comment


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
    previous_article_id = serializers.IntegerField(read_only=True)
    next_article_id = serializers.IntegerField(read_only=True)

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
            'previous_article_id',
            'next_article_id',
        )
