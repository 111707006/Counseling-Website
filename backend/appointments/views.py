import hashlib
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, api_view, permission_classes
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
        """
        根據不同的 action 設定權限
        """
        # 建立預約和查詢預約：允許匿名用戶（預約即註冊機制）
        if self.action in ['create', 'query']:
            permission_classes = [AllowAny]
        
        # 取消預約：需要身份驗證且為預約擁有者
        elif self.action == 'destroy':
            permission_classes = [AllowAny]  # 暫時改為AllowAny，因為用戶沒有JWT token
        
        # 更新預約狀態（確認/拒絕）：僅管理員
        elif self.action in ['update_status', 'confirm_appointment_time']:
            permission_classes = [IsAdminUser]
        
        # 獲取待確認預約列表：僅管理員
        elif self.action == 'pending_appointments':
            permission_classes = [IsAdminUser]
        
        # 其他操作（list, retrieve）：需要身份驗證
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

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
        # 使用CreateSerializer驗證和創建預約
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 驗證資料格式
        appointment = serializer.save()  # 儲存預約（會自動發送通知）
        
        # 設定回應標頭
        headers = self.get_success_headers(serializer.data)
        
        # 返回完整的預約資訊（使用AppointmentSerializer格式化）
        return Response(
            AppointmentSerializer(appointment).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=True, methods=['post'], url_path='cancel', permission_classes=[AllowAny])
    def cancel_appointment(self, request, pk=None):
        """
        取消預約的API端點（使用Email + 身分證驗證）
        POST /api/appointments/{id}/cancel/
        Body: {
            "email": "user@example.com",
            "id_number": "A123456789"
        }
        """
        # 獲取要取消的預約物件
        appointment = self.get_object()
        
        # 從請求中獲取驗證資料
        email = request.data.get('email')
        raw_id = request.data.get('id_number')
        
        # 驗證必要參數
        if not email or not raw_id:
            return Response(
                {'error': '請提供 email 與 id_number'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 驗證身份：檢查Email和身分證是否匹配預約用戶
        if appointment.user.email != email:
            return Response(
                {'error': '電子郵件不符'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not appointment.user.check_id_number(raw_id):
            return Response(
                {'error': '身分證號不符'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 檢查預約狀態：只有pending狀態的預約可以被取消
        if appointment.status != 'pending':
            return Response(
                {'error': '只有待確認的預約可以取消'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新預約狀態為cancelled而不是直接刪除
        appointment.status = 'cancelled'
        appointment.save()
        
        # 發送取消通知給管理員或心理師
        from .notifications import send_appointment_cancelled_notification
        try:
            send_appointment_cancelled_notification(appointment)
        except Exception as e:
            # 通知發送失敗不影響取消操作，只記錄錯誤
            print(f"取消通知發送失敗: {e}")
        
        # 如果預約已經有確認的時段，釋放該時段
        if appointment.slot:
            appointment.slot.is_booked = False  # 標記時段為可用
            appointment.slot.save()  # 儲存時段狀態
            appointment.slot = None  # 移除預約與時段的關聯
            appointment.save()  # 儲存預約變更
        
        # 返回成功訊息
        return Response(
            {'message': '預約已成功取消'}, 
            status=status.HTTP_200_OK
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
        
        print(f"DEBUG: 查詢預約 - Email: {email}, ID: {raw_id}")
        
        if not email or not raw_id:
            return Response({'error': '請提供 email 與 id_number'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, email=email)
            print(f"DEBUG: 找到用戶: {user.email}")
            
            if not user.check_id_number(raw_id):
                print(f"DEBUG: 身分證驗證失敗")
                return Response({'error': '身分證號不符'}, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"DEBUG: 身分證驗證成功")
        
            qs = Appointment.objects.filter(user=user).order_by('-created_at')
            print(f"DEBUG: 找到 {qs.count()} 筆預約")
            
            page = self.paginate_queryset(qs)
            serializer = AppointmentSerializer(page or qs, many=True)
            print(f"DEBUG: 序列化完成")
            
            if page is not None:
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"DEBUG: 查詢預約發生錯誤: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({'error': f'查詢失敗: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """
        更新預約狀態的API端點（管理員專用）
        PATCH /api/appointments/{id}/status/
        Body: {
            "status": "rejected",
            "rejection_reason": "時間無法配合"  # 拒絕時的原因（可選）
        }
        """
        # 獲取要更新的預約物件
        appointment = self.get_object()
        # 從請求中獲取新狀態
        new_status = request.data.get('status')
        # 從請求中獲取拒絕原因（如果是rejected狀態）
        rejection_reason = request.data.get('rejection_reason', '')
        
        # 驗證狀態是否有效
        if new_status not in dict(Appointment.STATUS_CHOICES):
            return Response({'error': '無效的狀態'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新預約狀態
        appointment.status = new_status
        appointment.save()
        
        # 如果狀態變更為rejected，發送拒絕通知給用戶
        if new_status == 'rejected':
            from .notifications import send_appointment_rejected_notification
            try:
                send_appointment_rejected_notification(appointment, rejection_reason)
            except Exception as e:
                # 通知發送失敗不影響狀態更新，只記錄錯誤
                print(f"拒絕通知發送失敗: {e}")
            
            # 取消排程的提醒郵件
            try:
                from .schedulers import cancel_appointment_reminders
                cancel_appointment_reminders(appointment)
            except Exception as e:
                print(f"取消郵件排程失敗: {e}")
            
            # 如果預約有確認的時段，釋放該時段
            if appointment.slot:
                appointment.slot.is_booked = False  # 標記時段為可用
                appointment.slot.save()  # 儲存時段狀態
                appointment.slot = None  # 移除預約與時段的關聯
                appointment.save()  # 儲存預約變更
        
        # 返回更新後的狀態
        return Response({
            'status': appointment.status,
            'message': f'預約狀態已更新為: {appointment.get_status_display()}'
        })

    @action(detail=True, methods=['post'], url_path='confirm-time', permission_classes=[IsAdminUser])
    def confirm_appointment_time(self, request, pk=None):
        """
        管理員/心理師確認預約時間的API端點
        HTTP方法: POST
        路徑: /api/appointments/{id}/confirm-time/
        權限: 僅管理員可使用
        請求格式: {
            "confirmed_datetime": "2025-08-02T09:30:00",  # ISO格式的確認時間
            "preferred_period_id": 123                    # 選擇的偏好時段ID（可選）
        }
        """
        # 根據URL中的pk參數獲取對應的預約物件
        appointment = self.get_object()
        # 從請求資料中提取確認時間字串
        confirmed_datetime_str = request.data.get('confirmed_datetime')
        # 從請求資料中提取偏好時段ID（目前未使用，保留擴展性）
        preferred_period_id = request.data.get('preferred_period_id')
        
        # 檢查必要參數：確認時間不能為空
        if not confirmed_datetime_str:
            return Response({'error': '請提供確認時間'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 使用try-except處理可能的錯誤
        try:
            # 導入所需的模組
            from datetime import datetime           # 用於時間解析
            from django.utils import timezone      # 用於時區處理
            from therapists.models import AvailableSlot  # 可用時段模型
            from .notifications import send_appointment_confirmed_notification  # 郵件通知函數
            
            # 解析並處理確認時間
            # 將ISO格式字串轉換為datetime物件，處理UTC時區標記
            confirmed_datetime = datetime.fromisoformat(confirmed_datetime_str.replace('Z', '+00:00'))
            # 如果時間是naive（無時區資訊），則設定為系統預設時區
            if timezone.is_naive(confirmed_datetime):
                confirmed_datetime = timezone.make_aware(confirmed_datetime)
            
            # 創建或獲取對應的AvailableSlot
            # get_or_create：如果存在則獲取，不存在則創建
            slot, created = AvailableSlot.objects.get_or_create(
                therapist=appointment.therapist,    # 預約的心理師
                slot_time=confirmed_datetime,       # 確認的時間
                defaults={'is_booked': True}        # 如果需要創建，預設為已預約狀態
            )
            
            # 檢查時段衝突：如果時段已存在且已被預約，則拒絕操作
            if not created and slot.is_booked:
                return Response({'error': '該時段已被預約'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 更新預約資訊
            appointment.slot = slot                    # 關聯到具體時段
            appointment.status = 'confirmed'           # 變更狀態為已確認
            appointment.confirmed_at = timezone.now()  # 記錄確認時間
            appointment.save()                         # 儲存變更
            
            # 標記時段為已預約（防止其他預約衝突）
            slot.is_booked = True
            slot.save()  # 儲存時段狀態
            
            # 發送確認通知給來談者
            try:
                # 調用郵件通知函數
                send_appointment_confirmed_notification(appointment, confirmed_datetime)
            except Exception as e:
                # 郵件發送失敗不影響預約確認，只記錄錯誤
                print(f"用戶確認通知發送失敗: {e}")
            
            # 發送確認通知給心理師
            try:
                from .notifications import send_therapist_appointment_confirmed
                send_therapist_appointment_confirmed(appointment, confirmed_datetime)
            except Exception as e:
                print(f"心理師確認通知發送失敗: {e}")
            
            # 安排提醒郵件
            try:
                from .schedulers import schedule_appointment_reminders
                schedule_appointment_reminders(appointment)
            except Exception as e:
                # 排程失敗不影響預約確認，只記錄錯誤
                print(f"郵件排程失敗: {e}")
            
            # 回傳成功響應
            return Response({
                'message': '預約時間確認成功',                # 成功訊息
                'appointment_id': appointment.id,             # 預約ID
                'confirmed_datetime': confirmed_datetime_str, # 確認的時間
                'status': appointment.status                  # 更新後的狀態
            })
            
        except ValueError as e:
            # 時間格式錯誤的處理
            return Response({'error': f'時間格式錯誤: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # 其他未預期錯誤的處理
            return Response({'error': f'確認失敗: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='pending', permission_classes=[IsAdminUser])
    def pending_appointments(self, request):
        """
        獲取待確認的預約列表（管理員/心理師專用）
        GET /api/appointments/pending/
        """
        user = request.user
        
        # 如果是心理師，只顯示自己的待確認預約
        if not (user.is_staff or user.is_superuser):
            from therapists.models import TherapistProfile
            try:
                therapist = TherapistProfile.objects.get(user=user)
                queryset = Appointment.objects.filter(
                    therapist=therapist,
                    status='pending'
                ).order_by('-created_at')
            except TherapistProfile.DoesNotExist:
                return Response({'error': '無權限查看'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # 管理員可以看到所有待確認預約
            queryset = Appointment.objects.filter(status='pending').order_by('-created_at')
        
        # 添加偏好時間資訊
        appointments_data = []
        for appointment in queryset:
            data = AppointmentSerializer(appointment).data
            
            # 添加偏好時間
            preferred_periods = []
            for period in appointment.preferred_periods.all():
                preferred_periods.append({
                    'id': period.id,
                    'date': period.date.strftime('%Y-%m-%d'),
                    'period': period.period,
                    'period_display': {
                        'morning': '上午 (09:00-12:00)',
                        'afternoon': '下午 (13:00-17:00)',
                        'evening': '晚上 (18:00-21:00)'
                    }.get(period.period, period.period)
                })
            
            data['preferred_periods'] = preferred_periods
            
            # 添加預約詳細資訊
            if hasattr(appointment, 'detail'):
                detail = appointment.detail
                data['detail'] = {
                    'name': detail.name,
                    'phone': detail.phone,
                    'main_concerns': detail.main_concerns,
                    'previous_therapy': detail.previous_therapy,
                    'urgency': detail.urgency,
                    'special_needs': detail.special_needs
                }
            
            appointments_data.append(data)
        
        return Response(appointments_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def test_appointment_create(request):
    """測試用的預約建立端點"""
    return Response({
        'message': 'Test endpoint works!', 
        'data_received': request.data
    })
