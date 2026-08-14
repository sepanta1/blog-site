from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    API is login-only. Any authenticated user can read (list/retrieve)
    any post, but only the post's author can update or delete it.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
       
        # Any authenticated user can read (GET/HEAD/OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only the author can write (POST/PUT/PATCH/DELETE)
        return obj.author == request.user
