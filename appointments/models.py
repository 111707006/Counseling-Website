from django.db import models
from django.conf import settings
from therapists.models import AvailableSlot, TherapistProfile

class Appointment(models.Model):
    """
    預約模型：記錄使用者對心理師的預約資訊
    """
    CONSULTATION_CHOICES = [
        ('online', '線上'),
        ('offline', '實體'),
    ]
    STATUS_CHOICES = [
        ('pending', '待確認'),
        ('confirmed', '已確認'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        help_text='預約的使用者'
    )
    therapist = models.ForeignKey(
        TherapistProfile,
        on_delete=models.CASCADE,
        related_name='appointments',
        help_text='預約的心理師'
    )
    slot = models.OneToOneField(
        AvailableSlot,
        on_delete=models.CASCADE,
        related_name='appointment',
        help_text='對應的可預約時段；被預約後自動標記為已預約'
    )
    consultation_type = models.CharField(
        max_length=20,
        choices=CONSULTATION_CHOICES,
        help_text='諮詢方式：線上或實體'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='預約狀態'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='建立時間'
    )

    def __str__(self):
        return f"{self.user.username} → {self.therapist.user.username} @{self.slot.start_time}"
