from decimal import Decimal
from django.db import models
from django.conf import settings
from therapists.models import AvailableSlot, TherapistProfile

class Appointment(models.Model):
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
        'therapists.TherapistProfile',
        on_delete=models.CASCADE,
        related_name='appointments',
        help_text='預約的心理師'
    )
    slot = models.OneToOneField(
        'therapists.AvailableSlot',
        on_delete=models.CASCADE,
        related_name='appointment',
        help_text='對應的可預約時段；被預約後自動標記為已預約'
    )
    consultation_type = models.CharField(
        max_length=20,
        choices=CONSULTATION_CHOICES,
        help_text='諮詢方式：線上或實體'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        help_text='預約當時的收費金額'
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

    def save(self, *args, **kwargs):
        if self.price in (None, Decimal('0'), ''):
            pricing_dict = getattr(self.therapist, 'pricing', {}) or {}
            self.price = pricing_dict.get(self.consultation_type, Decimal('0.00'))
        super().save(*args, **kwargs)

        if not self.slot.is_booked:
            self.slot.is_booked = True
            self.slot.save(update_fields=['is_booked'])

    def delete(self, *args, **kwargs):
        slot = self.slot
        super().delete(*args, **kwargs)
        slot.is_booked = False
        slot.save(update_fields=['is_booked'])

    def __str__(self):
        return f"{self.user.email} → {self.therapist.name} @ {self.slot.start_time}"
