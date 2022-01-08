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


class StringListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list('name', flat=True)


class ArticleListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    tags = StringListField()

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'body',
            'created_at',
            'updated_at',
            'comments_count',
            'tags',
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    previous_article_id = serializers.IntegerField(read_only=True)
    next_article_id = serializers.IntegerField(read_only=True)
    tags = StringListField()
    similar_articles = serializers.ListField(read_only=True)

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
            'tags',
            'previous_article_id',
            'next_article_id',
            'similar_articles',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = super().create(validated_data)
        instance.tags.set(*tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance = super().create(validated_data)
        instance.tags.set(*tags)
        return instance
