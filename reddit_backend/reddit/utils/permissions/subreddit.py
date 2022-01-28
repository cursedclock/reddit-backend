from rest_framework.permissions import BasePermission


class SubredditPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action == 'update':
            is_owner = request.user == obj.owner
            is_admin = request.user in obj.admins
            return is_owner or is_admin
        elif view.action == 'destroy':
            is_owner = request.user == obj.owner
            return is_owner
        return True
