# from rest_framework import viewsets, mixins, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from .models import Appointment
# from .serializers import AppointmentSerializer, AppointmentCreateSerializer
# from users.models import User

# class AppointmentViewSet(
#         mixins.ListModelMixin,
#         mixins.RetrieveModelMixin,
#         viewsets.GenericViewSet):
#     """
#     GET    /api/appointments/           列表（需 email+id_number 查詢―另有 lookup）
#     GET    /api/appointments/{id}/      檢視
#     """
#     queryset = Appointment.objects.all().order_by('-created_at')
#     serializer_class = AppointmentSerializer
#     permission_classes = [AllowAny]

#     @action(detail=False, methods=['post'], url_path='create', permission_classes=[AllowAny])
#     def create_appointment(self, request):
#         """
#         POST /api/appointments/create/
#         建立預約（同時處理預約即註冊邏輯）。
#         """
#         serializer = AppointmentCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         appointment = serializer.save()
#         return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)

#     @action(detail=False, methods=['post'], url_path='lookup', permission_classes=[AllowAny])
#     def lookup(self, request):
#         """
#         POST /api/appointments/lookup/
#         使用 email + id_number 查詢該使用者的所有預約。
#         """
#         email = request.data.get('email')
#         id_number = request.data.get('id_number')
#         if not email or not id_number:
#             return Response({'detail': 'email 與 id_number 為必填'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'detail': '用戶不存在'}, status=status.HTTP_404_NOT_FOUND)

#         if not user.check_id_number(id_number):
#             return Response({'detail': '身分證號驗證失敗'}, status=status.HTTP_403_FORBIDDEN)

#         queryset = Appointment.objects.filter(user=user).order_by('-created_at')
#         data = AppointmentSerializer(queryset, many=True).data
#         return Response(data)
