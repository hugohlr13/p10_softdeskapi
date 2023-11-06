from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Project


class Contributor(models.Model):
    """
    This model represents a contributor in the system. Each contributor is a user who is associated with a project.
    """

    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    @receiver(post_save, sender=Project)
    def create_author_contributor(sender, instance, created, **kwargs):
        """Creates a contributor instance automatically when a new project is created."""
        if created:
            Contributor.objects.create(
                user_id=instance.author_user_id, project_id=instance
            )
