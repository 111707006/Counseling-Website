from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils import timezone
from decimal import Decimal

from .models import Appointment, PreferredPeriod, AppointmentDetail, ScheduledEmail
from .forms import AppointmentAdminForm
from therapists.models import TherapistProfile, AvailableSlot
from .notifications import (
    send_appointment_confirmed_notification,
    send_appointment_rejected_notification,
    send_appointment_cancelled_notification
)


class PreferredPeriodInline(admin.TabularInline):
    """預約偏好時段的內嵌管理"""
    model = PreferredPeriod
    extra = 0
    readonly_fields = ('date', 'period', 'get_period_display')
    can_delete = False
    
    def get_period_display(self, obj):
        return obj.get_period_display()
    get_period_display.short_description = "時段顯示"


class AppointmentDetailInline(admin.StackedInline):
    """預約詳細資訊的內嵌管理"""
    model = AppointmentDetail
    extra = 0
    readonly_fields = ('name', 'phone', 'main_concerns', 'previous_therapy', 
                      'urgency', 'special_needs', 'specialty_requested')
    can_delete = False
    
    fieldsets = (
        ('用戶資訊', {
            'fields': ('name', 'phone')
        }),
        ('諮商需求', {
            'fields': ('main_concerns', 'previous_therapy', 'urgency', 'special_needs')
        }),
        ('專業需求', {
            'fields': ('specialty_requested',)
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentAdminForm
    list_display = (
        'id', 'get_user_info', 'get_therapist_name', 'consultation_type_display',
        'get_room_display', 'status_display', 'attendance_status_display', 
        'created_at', 'confirmed_at', 'get_action_buttons'
    )
    
    list_filter = (
        'status', 'attendance_status', 'consultation_type', 'consultation_room', 
        'therapist', 'created_at'
    )
    
    search_fields = (
        'user__email', 'detail__name', 'detail__phone', 
        'therapist__name', 'detail__main_concerns', 'admin_notes'
    )
    
    ordering = ('-created_at',)
    
    readonly_fields = (
        'user', 'created_at', 'confirmed_at', 'get_user_detail_info',
        'get_preferred_periods_display'
    )
    
    inlines = [AppointmentDetailInline, PreferredPeriodInline]
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('user', 'get_user_detail_info', 'consultation_type', 'status')
        }),
        ('心理師分配', {
            'fields': ('therapist', 'slot')
        }),
        ('諮商安排', {
            'fields': ('consultation_room', 'admin_notes'),
            'classes': ('collapse',),
        }),
        ('出席管理', {
            'fields': ('attendance_status', 'attendance_time'),
            'classes': ('collapse',),
        }),
        ('偏好時段', {
            'fields': ('get_preferred_periods_display',),
            'classes': ('collapse',),
        }),
        ('時間記錄', {
            'fields': ('created_at', 'confirmed_at'),
            'classes': ('collapse',),
        }),
    )
    
    # 自定義 URLs
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('calendar/', 
                 self.admin_site.admin_view(self.calendar_view),
                 name='appointments_appointment_calendar'),
            path('<int:appointment_id>/assign_therapist/', 
                 self.admin_site.admin_view(self.assign_therapist_view),
                 name='appointments_appointment_assign_therapist'),
            path('<int:appointment_id>/confirm_time/',
                 self.admin_site.admin_view(self.confirm_time_view), 
                 name='appointments_appointment_confirm_time'),
        ]
        return custom_urls + urls
    
    # ===== 顯示方法 =====
    
    def get_user_info(self, obj):
        """顯示用戶基本資訊"""
        if hasattr(obj, 'detail') and obj.detail.name:
            return f"{obj.detail.name} ({obj.user.email})"
        return obj.user.email
    get_user_info.short_description = "用戶資訊"
    
    def get_therapist_name(self, obj):
        """顯示心理師姓名"""
        if obj.therapist:
            return obj.therapist.name
        return format_html('<span style="color: red;">待分配</span>')
    get_therapist_name.short_description = "心理師"
    
    def consultation_type_display(self, obj):
        """諮商方式顯示"""
        return obj.get_consultation_type_display()
    consultation_type_display.short_description = "諮商方式"
    
    def status_display(self, obj):
        """狀態顯示（帶顏色）"""
        colors = {
            'pending': 'orange',
            'confirmed': 'green', 
            'completed': 'blue',
            'cancelled': 'gray',
            'rejected': 'red'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = "狀態"
    
    def attendance_status_display(self, obj):
        """出席狀態顯示（帶顏色）"""
        colors = {
            'pending': '#ffa500',    # 橘色
            'attended': '#28a745',   # 綠色
            'no_show': '#dc3545',    # 紅色
            'leave': '#6f42c1',      # 紫色
        }
        icons = {
            'pending': '⏳',
            'attended': '✅',
            'no_show': '❌',
            'leave': '📝',
        }
        color = colors.get(obj.attendance_status, 'black')
        icon = icons.get(obj.attendance_status, '❓')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, icon, obj.get_attendance_status_display()
        )
    attendance_status_display.short_description = "出席狀態"
    
    def get_room_display(self, obj):
        """顯示諮商室"""
        if obj.consultation_room:
            return obj.get_consultation_room_display()
        return '-'
    get_room_display.short_description = "諮商室"
    
    def get_user_detail_info(self, obj):
        """顯示用戶詳細資訊"""
        if hasattr(obj, 'detail'):
            detail = obj.detail
            info = f"姓名: {detail.name}<br>"
            info += f"電話: {detail.phone}<br>"
            info += f"主要關注議題: {detail.main_concerns[:50]}{'...' if len(detail.main_concerns) > 50 else ''}<br>"
            info += f"曾接受心理諮商: {'是' if detail.previous_therapy else '否'}<br>"
            info += f"緊急程度: {detail.get_urgency_display()}"
            if detail.special_needs:
                info += f"<br>特殊需求: {detail.special_needs[:50]}{'...' if len(detail.special_needs) > 50 else ''}"
            return format_html(info)
        return "無詳細資料"
    get_user_detail_info.short_description = "用戶詳細資訊"
    
    def get_preferred_periods_display(self, obj):
        """顯示偏好時段"""
        periods = obj.preferred_periods.all()
        if periods:
            period_list = []
            for period in periods:
                period_list.append(f"{period.date} {period.get_period_display()}")
            return format_html("<br>".join(period_list))
        return "無偏好時段"
    get_preferred_periods_display.short_description = "偏好時段"
    
    def get_action_buttons(self, obj):
        """顯示操作按鈕"""
        buttons = []
        
        # 編輯預約按鈕
        edit_url = reverse('admin:appointments_appointment_change', args=[obj.id])
        buttons.append(f'<a href="{edit_url}" class="button">編輯預約</a>')
        
        if obj.status == 'pending':
            # 分配心理師按鈕
            if not obj.therapist:
                assign_url = reverse('admin:appointments_appointment_assign_therapist', 
                                   args=[obj.id])
                buttons.append(f'<a href="{assign_url}" class="button">分配心理師</a>')
            
            # 確認時間按鈕
            if obj.therapist:
                confirm_url = reverse('admin:appointments_appointment_confirm_time',
                                    args=[obj.id])
                buttons.append(f'<a href="{confirm_url}" class="button">確認時間</a>')
        
        return format_html(" ".join(buttons))
    get_action_buttons.short_description = "操作"
    
    # ===== 自定義保存方法 =====
    
    def save_model(self, request, obj, form, change):
        """當在編輯頁面保存時的自定義處理"""
        from django.utils import timezone
        
        # 處理出席狀態變化
        if change and 'attendance_status' in form.changed_data:
            # 如果出席狀態有變化，記錄時間
            if obj.attendance_status != 'pending':
                obj.attendance_time = timezone.now()
        
        # 如果是修改（不是新建）並且狀態有變化
        if change and 'status' in form.changed_data:
            old_status = Appointment.objects.get(pk=obj.pk).status
            new_status = obj.status
            
            # 保存對象
            super().save_model(request, obj, form, change)
            
            # 根據新狀態發送相應的通知郵件
            try:
                if new_status == 'rejected':
                    send_appointment_rejected_notification(obj, "狀態已更新為拒絕")
                    messages.success(request, f'預約狀態已更新為「{obj.get_status_display()}」，已發送通知郵件給用戶')
                elif new_status == 'cancelled':
                    send_appointment_cancelled_notification(obj)
                    messages.success(request, f'預約狀態已更新為「{obj.get_status_display()}」，已發送通知郵件')
                else:
                    messages.success(request, f'預約狀態已更新為「{obj.get_status_display()}」')
                    
                # 如果拒絕或取消，釋放時段
                if new_status in ['rejected', 'cancelled'] and obj.slot:
                    obj.slot.is_booked = False
                    obj.slot.save()
                    obj.slot = None
                    obj.save()
                    
                    # 取消排程的提醒郵件
                    from .schedulers import cancel_appointment_reminders
                    cancel_appointment_reminders(obj)
                    
            except Exception as e:
                messages.warning(request, f'狀態更新成功，但郵件發送失敗: {e}')
        else:
            # 正常保存
            super().save_model(request, obj, form, change)
            
        # 如果有出席狀態變化，顯示訊息
        if change and 'attendance_status' in form.changed_data:
            messages.success(request, f'出席狀態已更新為「{obj.get_attendance_status_display()}」')
    
    # ===== 自定義視圖 =====
    
    def assign_therapist_view(self, request, appointment_id):
        """心理師分配功能"""
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        if request.method == 'POST':
            therapist_id = request.POST.get('therapist')
            if therapist_id:
                therapist = get_object_or_404(TherapistProfile, id=therapist_id)
                appointment.therapist = therapist
                
                
                appointment.save()
                
                messages.success(request, f'已成功分配心理師：{therapist.name}')
                return redirect('admin:appointments_appointment_change', appointment.id)
        
        # 獲取可用的心理師
        available_therapists = TherapistProfile.objects.all()
        
        # 如果有專業需求，優先推薦相關心理師
        recommended_therapists = []
        if hasattr(appointment, 'detail') and appointment.detail.specialty_requested:
            from therapists.models import Specialty
            try:
                specialty = Specialty.objects.get(id=appointment.detail.specialty_requested)
                recommended_therapists = specialty.therapists.all()
            except Specialty.DoesNotExist:
                pass
        
        context = {
            'title': f'分配心理師 - 預約 #{appointment.id}',
            'appointment': appointment,
            'available_therapists': available_therapists,
            'recommended_therapists': recommended_therapists,
            'opts': self.model._meta,
        }
        
        return TemplateResponse(request, 'admin/appointments/assign_therapist.html', context)
    
    def confirm_time_view(self, request, appointment_id):
        """時段確認功能"""
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        if not appointment.therapist:
            messages.error(request, '請先分配心理師')
            return redirect('admin:appointments_appointment_change', appointment.id)
        
        if request.method == 'POST':
            confirmed_datetime = request.POST.get('confirmed_datetime')
            if confirmed_datetime:
                from datetime import datetime
                from django.utils import timezone as tz
                
                try:
                    # 解析時間
                    dt = datetime.fromisoformat(confirmed_datetime.replace('T', ' '))
                    if tz.is_naive(dt):
                        dt = tz.make_aware(dt)
                    
                    # 創建或獲取時段
                    slot, created = AvailableSlot.objects.get_or_create(
                        therapist=appointment.therapist,
                        slot_time=dt,
                        defaults={'is_booked': True}
                    )
                    
                    if not created and slot.is_booked:
                        messages.error(request, '該時段已被預約')
                        return redirect(request.path)
                    
                    # 更新預約
                    appointment.slot = slot
                    appointment.status = 'confirmed'
                    appointment.confirmed_at = timezone.now()
                    appointment.save()
                    
                    # 標記時段為已預約
                    slot.is_booked = True
                    slot.save()
                    
                    # 發送確認通知
                    try:
                        send_appointment_confirmed_notification(appointment, dt)
                        messages.success(request, '預約時間確認成功，已發送通知郵件')
                    except Exception as e:
                        messages.warning(request, f'預約時間確認成功，但郵件發送失敗: {e}')
                    
                    return redirect('admin:appointments_appointment_change', appointment.id)
                    
                except ValueError as e:
                    messages.error(request, f'時間格式錯誤: {e}')
        
        # 獲取偏好時段
        preferred_periods = appointment.preferred_periods.all()
        
        context = {
            'title': f'確認預約時間 - 預約 #{appointment.id}',
            'appointment': appointment,
            'preferred_periods': preferred_periods,
            'opts': self.model._meta,
        }
        
        return TemplateResponse(request, 'admin/appointments/confirm_time.html', context)
    
    def calendar_view(self, request):
        """日曆排程系統"""
        from django.db.models import Q
        from datetime import datetime, timedelta
        import json
        from django.core.serializers.json import DjangoJSONEncoder
        
        # 獲取篩選參數
        therapist_filter = request.GET.get('therapist', '')
        room_filter = request.GET.get('room', '')
        consultation_type_filter = request.GET.get('consultation_type', '')
        
        # 基本查詢：只顯示已確認的預約
        queryset = Appointment.objects.filter(status='confirmed').select_related(
            'user', 'therapist', 'slot', 'detail'
        )
        
        # 應用篩選條件
        if therapist_filter:
            queryset = queryset.filter(therapist_id=therapist_filter)
        if room_filter:
            queryset = queryset.filter(consultation_room=room_filter)
        if consultation_type_filter:
            queryset = queryset.filter(consultation_type=consultation_type_filter)
        
        # 準備日曆事件數據
        events = []
        
        # 出席狀態顏色配置
        attendance_colors = {
            'pending': '#ffa500',    # 橘色
            'attended': '#28a745',   # 綠色
            'no_show': '#dc3545',    # 紅色
            'leave': '#6f42c1',      # 紫色
            'default': '#667eea'     # 預設藍色
        }
        
        for appointment in queryset:
            # 檢查是否有時間槽，如果沒有就使用預設時間
            if appointment.slot and appointment.slot.slot_time:
                # 有完整時間資訊的預約
                start_time = appointment.slot.slot_time
                end_time = start_time + timedelta(hours=1)
            else:
                # 沒有時間槽的預約，使用今天的預設時間顯示
                from django.utils import timezone
                today = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)
                start_time = today
                end_time = today + timedelta(hours=1)
            
            # 根據出席狀態設定事件顏色
            attendance_status = appointment.attendance_status
            color = attendance_colors.get(attendance_status, attendance_colors['default'])
            
            event = {
                'id': appointment.id,
                'title': f"{appointment.detail.name if hasattr(appointment, 'detail') and appointment.detail.name else appointment.user.email}",
                'start': start_time.isoformat(),
                'end': end_time.isoformat(),
                'backgroundColor': color,
                'borderColor': color,
                'extendedProps': {
                    'appointmentId': appointment.id,
                    'therapist': appointment.therapist.name if appointment.therapist else '待分配心理師',
                    'therapistId': appointment.therapist.id if appointment.therapist else None,
                    'room': appointment.get_consultation_room_display() if appointment.consultation_room else '待分配諮商室',
                    'phone': appointment.detail.phone if hasattr(appointment, 'detail') else '',
                    'email': appointment.user.email,
                    'consultationType': appointment.get_consultation_type_display(),
                    'notes': appointment.admin_notes or '',
                    'status': appointment.get_status_display(),
                    'hasSlot': bool(appointment.slot and appointment.slot.slot_time),
                    'attendanceStatus': appointment.get_attendance_status_display(),
                    'attendanceStatusCode': appointment.attendance_status,
                    'attendanceTime': appointment.attendance_time.isoformat() if appointment.attendance_time else None
                }
            }
            events.append(event)
        
        # 獲取篩選選項
        therapists_list = TherapistProfile.objects.all()
        room_choices = Appointment.ROOM_CHOICES
        consultation_type_choices = Appointment.CONSULTATION_CHOICES
        
        context = {
            'title': '預約日曆排程系統',
            'events': json.dumps(events, cls=DjangoJSONEncoder),
            'attendance_colors': json.dumps(attendance_colors),
            'therapists': therapists_list,
            'room_choices': room_choices,
            'consultation_type_choices': consultation_type_choices,
            'filters': {
                'therapist': therapist_filter,
                'room': room_filter,
                'consultation_type': consultation_type_filter
            },
            'opts': self.model._meta,
            'has_view_permission': True,
            'has_add_permission': True,
            'has_change_permission': True,
        }
        
        return TemplateResponse(request, 'admin/appointments/calendar.html', context)
    
    def update_status_view(self, request, appointment_id):
        """狀態管理功能"""
        print(f"DEBUG: Accessing update_status_view for appointment_id: {appointment_id}")
        print(f"DEBUG: Request method: {request.method}")
        print(f"DEBUG: User: {request.user}")
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        if request.method == 'POST':
            new_status = request.POST.get('status')
            rejection_reason = request.POST.get('rejection_reason', '')
            
            if new_status in dict(Appointment.STATUS_CHOICES):
                old_status = appointment.status
                appointment.status = new_status
                appointment.save()
                
                # 發送相應的通知郵件
                try:
                    if new_status == 'rejected':
                        send_appointment_rejected_notification(appointment, rejection_reason)
                        messages.success(request, '預約已拒絕，已發送通知郵件')
                    elif new_status == 'cancelled':
                        send_appointment_cancelled_notification(appointment)
                        messages.success(request, '預約已取消，已發送通知郵件')
                    else:
                        messages.success(request, f'預約狀態已更新為：{appointment.get_status_display()}')
                        
                except Exception as e:
                    messages.warning(request, f'狀態更新成功，但郵件發送失敗: {e}')
                
                # 如果拒絕或取消，釋放時段
                if new_status in ['rejected', 'cancelled'] and appointment.slot:
                    appointment.slot.is_booked = False
                    appointment.slot.save()
                    appointment.slot = None
                    appointment.save()
                
                return redirect('admin:appointments_appointment_change', appointment.id)
        
        context = {
            'title': f'管理預約狀態 - 預約 #{appointment.id}',
            'appointment': appointment,
            'status_choices': Appointment.STATUS_CHOICES,
            'opts': self.model._meta,
        }
        
        return TemplateResponse(request, 'admin/appointments/update_status.html', context)
    
    # ===== 列表視圖自定義 =====
    
    def get_queryset(self, request):
        """優化查詢效能"""
        return super().get_queryset(request).select_related(
            'user', 'therapist', 'slot', 'detail'
        ).prefetch_related('preferred_periods')
    
    def changelist_view(self, request, extra_context=None):
        """自定義列表視圖，添加統計資訊"""
        # 獲取統計資訊
        queryset = self.get_queryset(request)
        stats = {
            'total': queryset.count(),
            'pending': queryset.filter(status='pending').count(),
            'confirmed': queryset.filter(status='confirmed').count(),
            'today_appointments': queryset.filter(
                created_at__date=timezone.now().date()
            ).count(),
        }
        
        extra_context = extra_context or {}
        extra_context['stats'] = stats
        
        return super().changelist_view(request, extra_context)


# 註冊相關模型（如果需要單獨管理）
@admin.register(PreferredPeriod)
class PreferredPeriodAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'date', 'period', 'get_period_display')
    list_filter = ('period', 'date')
    search_fields = ('appointment__user__email', 'appointment__detail__name')
    readonly_fields = ('appointment', 'date', 'period')


@admin.register(AppointmentDetail)
class AppointmentDetailAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'name', 'phone', 'urgency', 'previous_therapy')
    list_filter = ('urgency', 'previous_therapy')
    search_fields = ('name', 'phone', 'main_concerns', 'appointment__user__email')
    readonly_fields = ('appointment',)
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('appointment', 'name', 'phone')
        }),
        ('諮商需求', {
            'fields': ('main_concerns', 'previous_therapy', 'urgency', 'special_needs')
        }),
        ('專業需求', {
            'fields': ('specialty_requested',)
        }),
    )


@admin.register(ScheduledEmail) 
class ScheduledEmailAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_appointment_info', 'email_type_display', 'recipient_email',
        'scheduled_time', 'status_display', 'sent_at', 'retry_count'
    )
    
    list_filter = (
        'email_type', 'status', 'scheduled_time', 'created_at'
    )
    
    search_fields = (
        'appointment__user__email', 'appointment__detail__name', 
        'recipient_email', 'appointment__id'
    )
    
    readonly_fields = (
        'appointment', 'email_type', 'recipient_email', 'scheduled_time',
        'sent_at', 'error_message', 'retry_count', 'created_at', 'updated_at'
    )
    
    ordering = ('-scheduled_time',)
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('appointment', 'email_type', 'recipient_email')
        }),
        ('排程資訊', {
            'fields': ('scheduled_time', 'status')
        }),
        ('執行結果', {
            'fields': ('sent_at', 'error_message', 'retry_count')
        }),
        ('時間記錄', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_appointment_info(self, obj):
        """顯示預約資訊"""
        appointment = obj.appointment
        if hasattr(appointment, 'detail') and appointment.detail.name:
            return f"#{appointment.id} - {appointment.detail.name}"
        return f"#{appointment.id} - {appointment.user.email}"
    get_appointment_info.short_description = "預約資訊"
    
    def email_type_display(self, obj):
        """郵件類型顯示"""
        return obj.get_email_type_display()
    email_type_display.short_description = "郵件類型"
    
    def status_display(self, obj):
        """狀態顯示（帶顏色）"""
        colors = {
            'pending': 'orange',
            'sent': 'green',
            'failed': 'red',
            'cancelled': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = "狀態"
    
    def get_queryset(self, request):
        """優化查詢效能"""
        return super().get_queryset(request).select_related(
            'appointment', 'appointment__user', 'appointment__detail'
        )
    
    def has_add_permission(self, request):
        """禁止手動添加排程郵件"""
        return False