from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User model that represents a user in the system.
    """

    age = models.PositiveIntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
