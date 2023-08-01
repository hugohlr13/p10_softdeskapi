from rest_framework import permissions

class ProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Si c'est une méthode en lecture seule, autoriser si l'utilisateur est l'auteur
        if request.method in permissions.SAFE_METHODS:
            return obj.author_user_id == request.user
        
        # Autoriser uniquement l'auteur pour les modifications
        return obj.author_user_id == request.user

class IssuePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Si c'est une méthode en lecture seule, autoriser si l'utilisateur est l'auteur ou l'assigné
        if request.method in permissions.SAFE_METHODS:
            return obj.author_user_id == request.user or obj.assignee_user_id == request.user

        # Autoriser uniquement l'auteur pour les modifications
        return obj.author_user_id == request.user

class CommentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Si c'est une méthode en lecture seule, autoriser si l'utilisateur est l'auteur de l'issue liée
        if request.method in permissions.SAFE_METHODS:
            return obj.issue_id.author_user_id == request.user
        
        # Autoriser uniquement l'auteur pour les modifications
        return obj.author_user_id == request.user
