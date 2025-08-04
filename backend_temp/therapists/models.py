from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# ═══════════════════════════════════════════════════════════════════
#  Specialty (專業領域)
# ═══════════════════════════════════════════════════════════════════
class Specialty(models.Model):
    """專業領域（如：認知行為治療、青少年諮商、創傷治療等）"""
    name = models.CharField(max_length=100, unique=True, help_text="專業領域名稱")
    description = models.TextField(blank=True, help_text="專業領域說明")
    is_active = models.BooleanField(default=True, help_text="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "專業領域"
        verbose_name_plural = "專業領域"
        ordering = ['name']
    
    def __str__(self):
        return self.name


# ═══════════════════════════════════════════════════════════════════
#  TherapistProfile
# ═══════════════════════════════════════════════════════════════════
class TherapistProfile(models.Model):
    """
    心理師個人介紹；前台團隊頁面會讀取此資料。
    """
    # 連到登入帳號（可為 NULL，表示尚未綁定）
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='therapistprofile',
        help_text="對應的 Django 使用者帳號"
    )

    # 基本欄位
    name            = models.CharField(max_length=100, help_text="姓名")
    title           = models.CharField(max_length=100, help_text="頭銜，如：諮商所督導")
    license_number  = models.CharField(max_length=50, help_text="證照字號")
    education       = models.TextField(help_text="學歷 / 證書")
    experience      = models.TextField(help_text="經歷描述")
    specialties     = models.ManyToManyField(
        Specialty, 
        related_name='therapists', 
        blank=True,
        help_text="專業領域（關聯式）"
    )
    # 保留舊的文字專長欄位供過渡期使用
    specialties_text = models.TextField(
        blank=True, 
        help_text="專長文字描述（舊格式，逐步淘汰）"
    )
    beliefs         = models.TextField(help_text="諮商信念 / 理念")
    publications    = models.JSONField(default=list, help_text="文章列表（字串陣列）")
    photo           = models.ImageField(upload_to='therapists/', null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    # 諮詢模式 & 收費
    CONSULTATION_CHOICES = [('online','線上'), ('offline','實體')]
    consultation_modes = models.JSONField(
        default=list,
        help_text="可提供諮詢模式，例如：['online','offline']"
    )
    pricing = models.JSONField(
        default=dict,
        help_text="各模式收費，如：{'online':1200,'offline':1500}"
    )

    # ───────── 驗證 ─────────
    def clean(self):
        super().clean()
        # 1) consultation_modes 只能包含合法選項
        illegal = [m for m in self.consultation_modes
                   if m not in dict(self.CONSULTATION_CHOICES)]
        if illegal:
            raise ValidationError({"consultation_modes": f"非法模式: {illegal}"})
        # 2) 每個模式都需有 pricing
        missing_price = [m for m in self.consultation_modes if m not in self.pricing]
        if missing_price:
            raise ValidationError({"pricing": f"缺少定價: {missing_price}"})
        # 3) 價格需 > 0
        for mode, price in self.pricing.items():
            if Decimal(price) <= 0:
                raise ValidationError({"pricing": f"{mode} 價格必須 > 0"})

    def get_specialties_display(self):
        """取得專業領域的顯示文字"""
        if self.specialties.exists():
            return ', '.join([specialty.name for specialty in self.specialties.all()])
        return self.specialties_text

    def get_specialties_list(self):
        """取得專業領域列表"""
        return [specialty.name for specialty in self.specialties.all()]

    def __str__(self):
        return self.name


# ═══════════════════════════════════════════════════════════════════
#  AvailableTime  (週期排班設定，可後續展開成 Slot)
# ═══════════════════════════════════════════════════════════════════
class AvailableTime(models.Model):
    WEEK_DAYS = [
        ('monday',   '週一'),
        ('tuesday',  '週二'),
        ('wednesday','週三'),
        ('thursday', '週四'),
        ('friday',   '週五'),
        ('saturday', '週六'),
        ('sunday',   '週日'),
    ]
    therapist   = models.ForeignKey(
        TherapistProfile, related_name='available_times',
        on_delete=models.CASCADE
    )
    day_of_week = models.CharField(max_length=9, choices=WEEK_DAYS)
    start_time  = models.TimeField()
    end_time    = models.TimeField()

    class Meta:
        ordering = ['therapist', 'day_of_week', 'start_time']
        unique_together = ('therapist','day_of_week','start_time','end_time')

    def __str__(self):
        return f"{self.therapist.name} — {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


# ═══════════════════════════════════════════════════════════════════
#  AvailableSlot  (實際某天某時段；被預約後 is_booked=True)
# ═══════════════════════════════════════════════════════════════════
class AvailableSlot(models.Model):
    therapist = models.ForeignKey(TherapistProfile, on_delete=models.CASCADE)
    slot_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['therapist', 'slot_time']
        unique_together = ('therapist','slot_time')

    def __str__(self):
        return f"{self.therapist.name} @ {self.slot_time}"
