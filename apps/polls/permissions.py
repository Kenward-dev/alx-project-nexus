"""
Custom permissions for the polling system.
"""
from rest_framework import permissions


class IsCreatorOrAdmin(permissions.BasePermission):
    """Allow actions only for the poll creator or admin user."""

    def has_object_permission(self, request, view, obj):
        """Check if user is creator or admin."""
        return request.user == obj.creator or request.user.is_staff


class IsDraftPoll(permissions.BasePermission):
    """Only allow edits/deletes for draft polls."""

    def has_object_permission(self, request, view, obj):
        """Check if poll is draft."""
        return obj.is_draft