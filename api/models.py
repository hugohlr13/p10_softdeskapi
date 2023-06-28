from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    This model represents a project in the system. Each project is created by a user, who becomes the author.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20)
    author_user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    """
    This model represents a contributor in the system. Each contributor is a user who is associated with a project.
    """
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)


class Issue(models.Model):
    """
    This model represents an issue in the system. Each issue belongs to a project and has a contributor (the author of the issue).
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.CharField(max_length=20)
    priority = models.CharField(max_length=20)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="To Do")
    author_user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assignee_user_id = models.ForeignKey(User, related_name='assigned_issues', on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    This model represents a comment in the system. Each comment is associated with an issue and has an author.
    """
    description = models.TextField()
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

