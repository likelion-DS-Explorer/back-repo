from rest_framework import permissions

class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_authenticated and request.user.is_manager

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated and request.user.is_manager