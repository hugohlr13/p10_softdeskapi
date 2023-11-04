from django.contrib import admin

from .models import Comment, Issue, Project

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
