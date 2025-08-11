from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils import timezone
from decimal import Decimal

from .models import Appointment, PreferredPeriod, AppointmentDetail
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
    list_display = (
        'id', 'get_user_info', 'get_therapist_name', 'consultation_type_display',
        'status_display', 'created_at', 'confirmed_at',
        'get_action_buttons'
    )
    
    list_filter = (
        'status', 'consultation_type', 'therapist', 'created_at'
    )
    
    search_fields = (
        'user__email', 'detail__name', 'detail__phone', 
        'therapist__name', 'detail__main_concerns'
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
        ('偏好時段', {
            'fields': ('get_preferred_periods_display',)
        }),
        ('時間記錄', {
            'fields': ('created_at', 'confirmed_at')
        }),
    )
    
    # 自定義 URLs
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:appointment_id>/assign_therapist/', 
                 self.admin_site.admin_view(self.assign_therapist_view),
                 name='appointments_appointment_assign_therapist'),
            path('<int:appointment_id>/confirm_time/',
                 self.admin_site.admin_view(self.confirm_time_view), 
                 name='appointments_appointment_confirm_time'),
            path('<int:appointment_id>/update_status/',
                 self.admin_site.admin_view(self.update_status_view),
                 name='appointments_appointment_update_status'),
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
            
            # 狀態管理按鈕
            status_url = reverse('admin:appointments_appointment_update_status',
                               args=[obj.id])
            buttons.append(f'<a href="{status_url}" class="button">管理狀態</a>')
        
        return format_html(" ".join(buttons))
    get_action_buttons.short_description = "操作"
    
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
    
    def update_status_view(self, request, appointment_id):
        """狀態管理功能"""
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