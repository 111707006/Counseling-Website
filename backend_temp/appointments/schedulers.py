"""
Email scheduling utilities for appointments
"""

from datetime import timedelta
from django.utils import timezone
from .models import ScheduledEmail, Appointment


def schedule_appointment_reminders(appointment: Appointment):
    """
    為預約安排提醒郵件
    當預約被確認時調用此函數
    僅安排預約前24小時提醒給用戶和心理師
    """
    if not appointment.slot or not appointment.slot.slot_time:
        return False
    
    appointment_time = appointment.slot.slot_time
    user_email = appointment.user.email
    
    # 24小時提醒 - 發送給用戶
    reminder_24h_time = appointment_time - timedelta(days=1)
    if reminder_24h_time > timezone.now():
        schedule_email(
            appointment=appointment,
            email_type='reminder_24h_user',
            recipient_email=user_email,
            scheduled_time=reminder_24h_time
        )
        print(f"已安排用戶24小時提醒: {user_email} @ {reminder_24h_time}")
    
    # 24小時提醒 - 發送給心理師
    if appointment.therapist and appointment.therapist.user and appointment.therapist.user.email:
        therapist_email = appointment.therapist.user.email
        schedule_email(
            appointment=appointment,
            email_type='reminder_24h_therapist',
            recipient_email=therapist_email,
            scheduled_time=reminder_24h_time
        )
        print(f"已安排心理師24小時提醒: {therapist_email} @ {reminder_24h_time}")
    
    return True


def schedule_email(appointment: Appointment, email_type: str, recipient_email: str, scheduled_time):
    """
    安排單一郵件發送
    """
    # 檢查是否已經存在相同類型的排程郵件
    existing_email = ScheduledEmail.objects.filter(
        appointment=appointment,
        email_type=email_type
    ).first()
    
    if existing_email:
        if existing_email.status == 'pending':
            # 更新現有的排程時間
            existing_email.scheduled_time = scheduled_time
            existing_email.recipient_email = recipient_email
            existing_email.save()
            print(f"更新排程郵件: {email_type} 到 {recipient_email} @ {scheduled_time}")
        else:
            print(f"排程郵件已存在且狀態為 {existing_email.status}: {email_type}")
        return existing_email
    
    # 創建新的排程郵件
    scheduled_email = ScheduledEmail.objects.create(
        appointment=appointment,
        email_type=email_type,
        recipient_email=recipient_email,
        scheduled_time=scheduled_time
    )
    
    print(f"新增排程郵件: {email_type} 到 {recipient_email} @ {scheduled_time}")
    return scheduled_email


def cancel_appointment_reminders(appointment: Appointment):
    """
    取消預約相關的所有未發送提醒郵件
    當預約被取消或修改時調用
    """
    cancelled_count = ScheduledEmail.objects.filter(
        appointment=appointment,
        status='pending'
    ).update(status='cancelled')
    
    if cancelled_count > 0:
        print(f"已取消 {cancelled_count} 封預約 {appointment.id} 的排程郵件")
    
    return cancelled_count


def reschedule_appointment_reminders(appointment: Appointment):
    """
    重新安排預約提醒郵件
    當預約時間被修改時調用
    """
    # 先取消現有的排程
    cancel_appointment_reminders(appointment)
    
    # 重新安排提醒
    return schedule_appointment_reminders(appointment)


def get_pending_reminders(appointment: Appointment = None):
    """
    獲取待發送的提醒郵件
    """
    queryset = ScheduledEmail.objects.filter(status='pending').order_by('scheduled_time')
    
    if appointment:
        queryset = queryset.filter(appointment=appointment)
    
    return queryset


def cleanup_old_scheduled_emails(days_old: int = 30):
    """
    清理舊的排程郵件記錄
    刪除指定天數前的已完成或已取消的郵件記錄
    """
    cutoff_date = timezone.now() - timedelta(days=days_old)
    
    deleted_count = ScheduledEmail.objects.filter(
        created_at__lt=cutoff_date,
        status__in=['sent', 'cancelled', 'failed']
    ).delete()
    
    print(f"清理了 {deleted_count[0]} 條舊的排程郵件記錄 (超過 {days_old} 天)")
    return deleted_count[0]