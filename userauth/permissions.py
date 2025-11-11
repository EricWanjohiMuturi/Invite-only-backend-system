from rest_framework import permissions

class IsAdminOrDirector(permissions.BasePermission):
    """Allow access only to users with role admin or director."""
    
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in ('admin', 'director')

class HasRolePermission(permissions.BasePermission):
    """Generic role-based permission checking.
    Use by passing allowed roles in view: `allowed_roles = ('marketing',)`
    """
    def has_permission(self, request, view):
        allowed = getattr(view, 'allowed_roles', None)
        if not allowed:
            return True
        return hasattr(request.user, 'role') and request.user.role in allowed