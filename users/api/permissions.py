from rest_framework import permissions

class IsAuthenticatedAndRequestOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user