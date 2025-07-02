from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Appointment
from .serializers import SlotSerializer, AppointmentSerializer, AppointmentCreateSerializer
from .permissions import IsUser, IsTherapist, IsAdmin

class AvailableSlotViewSet(viewsets.ReadOnlyModelViewSet):
    """
    心理師可預約時段查詢
    GET /api/appointments/slots/?therapist=<id>
    """
    serializer_class = SlotSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # 根據 query param 篩選尚未被預約的時段
        therapist_id = self.request.query_params.get('therapist')
        qs = self.get_serializer().Meta.model.objects.filter(is_booked=False)
        if therapist_id:
            qs = qs.filter(therapist__id=therapist_id)
        return qs

class AppointmentViewSet(viewsets.GenericViewSet,
                         viewsets.mixins.ListModelMixin,
                         viewsets.mixins.RetrieveModelMixin,
                         viewsets.mixins.DestroyModelMixin):
    """
    預約管理 API
    - list / retrieve 由 role 決定範圍
    - create 由 AppointmentCreateSerializer 處理
    - destroy 取消預約並釋放時段
    - update 狀態由 therapist/admin 控制
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        動態選擇權限：
        - create 僅 user
        - 自己取消僅 user
        - therapist/admin 可更新狀態
        - list/retrieve 需登入
        """
        if self.action == 'create':
            return [IsUser()]
        if self.action in ['therapist_appointments', 'my']:
            return [IsAuthenticated()]
        if self.action in ['update_status']:
            return [IsTherapist() | IsAdmin()]
        if self.action == 'destroy':
            return [IsUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        # 選擇不同場景使用不同 Serializer
        if self.action == 'create':
            return AppointmentCreateSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        # 一般使用者只能看自己的預約
        if user.role == 'user':
            return Appointment.objects.filter(user=user)
        # 心理師只能看自己被預約的
        if user.role == 'therapist':
            return Appointment.objects.filter(therapist__user=user)
        # 管理員可看所有
        if user.role == 'admin':
            return Appointment.objects.all()
        return Appointment.objects.none()

    def create(self, request, *args, **kwargs):
        """POST /api/appointments/"""
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='my')
    def my(self, request):
        """
        GET /api/appointments/my/
        取得當前使用者的預約清單
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='therapist')
    def therapist_appointments(self, request):
        """
        GET /api/appointments/therapist/
        心理師查看所有屬於自己的預約
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """
        PATCH /api/appointments/{id}/status/
        心理師或管理員更新預約狀態
        """
        appointment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Appointment.STATUS_CHOICES):
            return Response({'error': '無效的狀態'}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = new_status
        # 若取消或完成，釋放時段
        if new_status in ['cancelled', 'completed']:
            slot = appointment.slot
            slot.is_booked = False
            slot.save()
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE /api/appointments/{id}/
        使用者自行取消預約，並釋放時段
        """
        appointment = self.get_object()
        slot = appointment.slot
        slot.is_booked = False
        slot.save()
        return super().destroy(request, *args, **kwargs)
