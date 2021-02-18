from rest_framework import serializers

from apps.strategies.models import Strategy


class StrategySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    compiled = serializers.BooleanField(read_only=True)

    class Meta:
        model = Strategy
        fields = '__all__'
