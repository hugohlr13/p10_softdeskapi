from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    User model that represents a user in the system.
    """
    age = models.PositiveIntegerField(null=True, blank=True)
