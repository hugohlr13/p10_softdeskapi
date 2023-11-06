from rest_framework import serializers

from .models import Comment, Issue, Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project objects, includes all fields."""

    class Meta:
        model = Project
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    """Serializer for Issue objects, includes all fields."""
    
    class Meta:
        model = Issue
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment objects, includes all fields."""

    class Meta:
        model = Comment
        fields = "__all__"
