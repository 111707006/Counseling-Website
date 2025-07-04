from rest_framework.permissions import BasePermission, IsAdminUser

class IsAppointmentOwner(BasePermission):
    """
    僅允許預約的 user 本人操作（例如取消）。
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user

class IsAdmin(IsAdminUser):
    """
    僅限管理員（staff 或 superuser）。
    """
    pass
