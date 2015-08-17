from rest_framework import permissions


class IsOwnerOrAnonOrReadOnly(permissions.BasePermission):
    """
        The object must have an attribute uploads_owner which may be null.
        Edit permissions are given only when request.user is owner
        or uploads_owner is null
    """

    def has_object_permission(self, request, view, object):
        if request.method in permissions.SAFE_METHODS:
            return True

        if object.uploads_owner is None:
            return True

        return object.uploads_owner == request.user
