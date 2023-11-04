from django.contrib import admin
from django.contrib.auth.models import \
    User  # Si c'est le modèle que vous utilisez pour l'authentification

from api.models import Project  # Import du modèle Project

from .models import Contributor


class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "project_id",
    )  # Assurez-vous que ces noms de champs correspondent à ceux dans votre modèle
    list_filter = ("project_id",)  # Le filtre par projet


admin.site.register(Contributor, ContributorAdmin)
