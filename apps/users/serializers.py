from rest_framework import serializers
from .models import SeptaUser


class UserDataSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SeptaUser
        fields = '__all__'
