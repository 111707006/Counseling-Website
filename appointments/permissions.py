from rest_framework.permissions import BasePermission

class IsUser(BasePermission):
    """
    僅限 role='user' 的使用者
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'

class IsTherapist(BasePermission):
    """
    僅限 role='therapist' 的心理師
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'therapist'

class IsAdmin(BasePermission):
    """
    僅限 role='admin' 的管理員
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
