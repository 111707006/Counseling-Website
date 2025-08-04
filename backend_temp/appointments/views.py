import hashlib
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from .permissions import IsAppointmentOwner, IsTherapistOwner
from therapists.models import TherapistProfile

User = get_user_model()

class AppointmentViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    POST   /api/appointments/           建立預約
    GET    /api/appointments/           列表（本人 or 管理員） 
    GET    /api/appointments/{id}/      檢視
    PATCH  /api/appointments/{id}/status/   更新狀態（僅管理員）
    DELETE /api/appointments/{id}/      取消（僅本人）
    POST   /api/appointments/query/     查詢預約（Email+身分證）
    """
    queryset = Appointment.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.action in ['create', 'query']:
            return [AllowAny()]

        if self.action == 'destroy':
            return [IsAuthenticated(), IsAppointmentOwner()]

        if self.action == 'update_status':
            return [IsAdminUser()]

        # list / retrieve 操作，區分不同角色的權限
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return [IsAdminUser()]

        # 心理師只能查看自己負責的預約
        from therapists.models import TherapistProfile
        if TherapistProfile.objects.filter(user=user).exists():
            return [IsAuthenticated(), IsTherapistOwner()]

        # 用戶只能查看自己的預約
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        # 管理員可以查看所有預約
        if user.is_staff or user.is_superuser:
            return Appointment.objects.all().order_by('-created_at')

        # 心理師：只能查看自己負責的預約
        from therapists.models import TherapistProfile
        if TherapistProfile.objects.filter(user=user).exists():
            return Appointment.objects.filter(therapist__user=user).order_by('-created_at')

        # 用戶：只能查看自己的預約
        return Appointment.objects.filter(user=user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            AppointmentSerializer(appointment).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['post'], url_path='query', permission_classes=[AllowAny])
    def query(self, request):
        """
        POST /api/appointments/query/
        body: {"email": "...", "id_number": "..."}
        回傳該用戶所有預約紀錄
        """
        email = request.data.get('email')
        raw_id = request.data.get('id_number')
        if not email or not raw_id:
            return Response({'error': '請提供 email 與 id_number'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        if not user.check_id_number(raw_id):
            return Response({'error': '身分證號不符'}, status=status.HTTP_400_BAD_REQUEST)

        qs = Appointment.objects.filter(user=user).order_by('-created_at')
        page = self.paginate_queryset(qs)
        serializer = AppointmentSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        appointment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Appointment.STATUS_CHOICES):
            return Response({'error': '無效的狀態'}, status=status.HTTP_400_BAD_REQUEST)
        appointment.status = new_status
        appointment.save()
        return Response({'status': appointment.status})
