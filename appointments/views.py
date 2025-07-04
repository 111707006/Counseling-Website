from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from .permissions import IsAppointmentOwner

class AppointmentViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    POST   /api/appointments/           建立預約
    GET    /api/appointments/           列表（本人 or 管理員可看全部）
    GET    /api/appointments/{id}/      檢視
    PATCH  /api/appointments/{id}/status/   更新狀態（僅管理員）
    DELETE /api/appointments/{id}/      取消（僅本人）
    """
    queryset = Appointment.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAppointmentOwner()]
        if self.action == 'update_status':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=user)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """
        管理員更新預約狀態：
        PATCH /api/appointments/{id}/status/  body: {"status": "confirmed"}
        """
        appointment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Appointment.STATUS_CHOICES):
            return Response({'error': '無效的狀態'}, status=400)
        appointment.status = new_status
        appointment.save()
        return Response({'status': appointment.status})
