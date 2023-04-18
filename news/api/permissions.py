from rest_framework import permissions

class IsAuthenticatedAndOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user