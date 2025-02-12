from rest_framework import permissions

class CheckBron(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.status == 'owner':
            return True
        if request.user.status == 'client' and obj.status_room == 'свободен':
            return True
        return False