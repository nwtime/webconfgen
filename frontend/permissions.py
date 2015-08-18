from rest_framework import permissions


class IsOwnerOrAnonOrReadOnly(permissions.BasePermission):
    """
        The upload must have an attribute uploads_owner which may be null.
        Edit permissions are given only when request.user is owner
        or uploads_owner is null
    """

    def has_object_permission(self, request, view, upload):
        if request.method in permissions.SAFE_METHODS:
            return True

        if upload.uploads_owner is None:
            return True

        return upload.uploads_owner == request.user
