from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user instances, translating between queryset or instance and JSON representation.
    Includes fields for identification, contact preferences, and age.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]  # JSON fields to be included in the serializer
