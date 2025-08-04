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
        null=True, blank=True,
        help_text='預約的心理師（可由管理員後續分配）'
    )
    slot = models.OneToOneField(
        'therapists.AvailableSlot',
        on_delete=models.CASCADE,
        related_name='appointment',
        null=True, blank=True,
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
    confirmed_at = models.DateTimeField(
        null=True, blank=True,
        help_text='確認時間'
    )

    def save(self, *args, **kwargs):
        if self.price in (None, Decimal('0'), ''):
            if self.therapist:
                pricing_dict = getattr(self.therapist, 'pricing', {}) or {}
                self.price = pricing_dict.get(self.consultation_type, Decimal('0.00'))
            else:
                # 如果沒有指定心理師，價格暫時設為0，待管理員分配心理師後再更新
                self.price = Decimal('0.00')
        super().save(*args, **kwargs)

        if self.slot and not self.slot.is_booked:
            self.slot.is_booked = True
            self.slot.save(update_fields=['is_booked'])

    def delete(self, *args, **kwargs):
        slot = self.slot
        super().delete(*args, **kwargs)
        if slot:
            slot.is_booked = False
            slot.save(update_fields=['is_booked'])

    def __str__(self):
        therapist_name = self.therapist.name if self.therapist else '待分配'
        time_info = self.slot.slot_time if self.slot else '待安排'
        return f"{self.user.email} → {therapist_name} @ {time_info}"


class PreferredPeriod(models.Model):
    """預約偏好時間"""
    PERIOD_CHOICES = [
        ('morning', '上午'),
        ('afternoon', '下午'),
        ('evening', '晚上'),
    ]

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='preferred_periods',
        help_text='對應的預約',
        null=True  # ✅ 加這行讓舊資料可以先不填
    )
    date = models.DateField(help_text='偏好日期')
    period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        help_text='偏好時段'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['appointment', 'date', 'period']
        ordering = ['date', 'period']

    def __str__(self):
        return f"{self.appointment.user.email} - {self.date} {self.get_period_display()}"


class AppointmentDetail(models.Model):
    """預約詳細資訊"""
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='detail',
        help_text='對應的預約'
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text='用戶姓名'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text='聯絡電話'
    )
    main_concerns = models.TextField(
        blank=True,
        default="",
        help_text='主要關注議題'
    )
    previous_therapy = models.BooleanField(
        default=False,
        help_text='是否曾接受過心理諮商'
    )
    urgency = models.CharField(
        max_length=20,
        choices=[
            ('low', '低'),
            ('medium', '中'),
            ('high', '高'),
        ],
        default='medium',
        help_text='緊急程度'
    )
    special_needs = models.TextField(
        blank=True,
        default="",
        help_text='特殊需求'
    )
    specialty_requested = models.IntegerField(
        null=True, blank=True,
        help_text='請求的專業領域ID'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment.user.email} - 詳細資訊"
