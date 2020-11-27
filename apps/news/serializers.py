from rest_framework import serializers

from .models import News


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'slug', 'publish')


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
