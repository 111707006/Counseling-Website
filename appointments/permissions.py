from rest_framework.permissions import BasePermission
from therapists.models import TherapistProfile

class IsAppointmentOwner(BasePermission):
    """
    僅允許預約的 user 本人操作（例如取消）。
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user

class IsTherapistOwner(BasePermission):
    """
    僅允許心理師查看／列出屬於自己的預約。
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            TherapistProfile.objects.filter(user=request.user).exists()
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            obj.therapist.user == request.user
        )
