# posts/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Works for Post and Comment (both have .author)
        return getattr(obj, "author_id", None) == getattr(request.user, "id", None)
