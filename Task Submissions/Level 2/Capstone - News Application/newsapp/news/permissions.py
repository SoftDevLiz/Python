"""
permissions.py – Custom DRF permission classes.

These are used in api_views.py to restrict endpoints by role.

Permission classes
------------------
  IsJournalist        – allows only users with role='journalist'
  IsEditor            – allows only users with role='editor'
  IsEditorOrJournalist – allows editors OR journalists
  IsReader            – allows only users with role='reader'
  IsOwnerOrEditor     – allows the object owner or any editor
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsJournalist(BasePermission):
    """Grant access only to authenticated journalists."""

    message = "Only journalists can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'journalist'
        )


class IsEditor(BasePermission):
    """Grant access only to authenticated editors."""

    message = "Only editors can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'editor'
        )


class IsEditorOrJournalist(BasePermission):
    """Grant access to editors and journalists (e.g. update / delete)."""

    message = "Only editors or journalists can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('editor', 'journalist')
        )


class IsReader(BasePermission):
    """Grant access only to readers."""

    message = "Only readers can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'reader'
        )


class IsOwnerOrEditor(BasePermission):
    """
    Object-level permission.

    - Safe (read) methods are allowed for all authenticated users.
    - Write methods are allowed if the user is the object's author OR an editor.
    """

    message = "You must be the author or an editor to modify this object."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # Check that the object has an 'author' field
        author = getattr(obj, 'author', None)
        return (
            request.user.role == 'editor'
            or (author and author == request.user)
        )
