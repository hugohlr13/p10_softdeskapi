from rest_framework import serializers

from .models import Contributor


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer for Contributor instances."""
    
    class Meta:
        model = Contributor
        fields = "__all__"
