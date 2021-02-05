from rest_framework import serializers

from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'body',
            'created',
            'updated',
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'body',
            'created',
            'updated',
        )
