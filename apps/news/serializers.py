from rest_framework import serializers

from apps.news.models import News
from apps.comments.serializers import CommentDetailSerializer


class NewsListSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField()

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'slug',
            'publish',
            'comment_count'
        ]


class NewsDetailSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField()
    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'slug',
            'publish',
            'comment_count',
            'comments'
        ]
