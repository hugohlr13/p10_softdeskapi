from django.contrib import admin
from django.contrib.auth.models import User  

from api.models import Project

from .models import Contributor


class ContributorAdmin(admin.ModelAdmin):
    """Admin interface for managing Contributor model data."""

    list_display = (
        "user_id",
        "project_id",
    )  
    list_filter = ("project_id",)


admin.site.register(Contributor, ContributorAdmin)
