from rest_framework import serializers

from .models import News


class NewsPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'slug', 'publish')


class NewsFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
