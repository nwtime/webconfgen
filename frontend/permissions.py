"""
Implements custom permissions for API access.

Implements IsOwnerOrAnonOrReadOnly for Upload API access.
"""


from rest_framework import permissions


class IsOwnerOrAnonOrReadOnly(permissions.BasePermission):
    """
        The upload must have an attribute uploads_owner which may be null.
        Edit permissions are given only when request.user is owner
        or uploads_owner is null.

        Usage is not defined fo upload which is not of type frontend.models.Upload
    """

    def has_object_permission(self, request, view, upload):
        """
            Grant permissions for all SAFE_METHODS.
            Grant permissions if uploads_owner is None.
            Grant permissions only to owner of file.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        if upload.uploads_owner is None:
            return True

        return upload.uploads_owner == request.user
