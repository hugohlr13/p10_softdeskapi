from uuid import uuid4

from django.conf import settings
from django.db import models


class Project(models.Model):
    """
    This model represents a project in the system. Each project is created by a user, who becomes the author.
    """

    TYPE_CHOICES = [
        ("back-end", "Back-End"),
        ("front-end", "Front-End"),
        ("iOS", "iOS"),
        ("Android", "Android"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Issue(models.Model):
    """
    This model represents an issue in the system. Each issue belongs to a project and has a contributor (the author of the issue).
    """

    TAG_CHOICES = [
        ("bug", "BUG"),
        ("feature", "FEATURE"),
        ("task", "TASK"),
    ]

    PRIORITY_CHOICES = [
        ("low", "LOW"),
        ("medium", "MEDIUM"),
        ("high", "HIGH"),
    ]

    STATUS_CHOICES = [
        ("to_do", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="To Do")
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    assignee_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="assigned_issues",
        on_delete=models.SET_NULL,
        null=True,
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    This model represents a comment in the system. Each comment is associated with an issue and has an author.
    """

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    description = models.TextField()
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_time = models.DateTimeField(auto_now_add=True)
