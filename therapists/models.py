from django.db import models

class TherapistProfile(models.Model):
    """
    心理師個人介紹資料模型，用於前台團隊頁面顯示。
    """
    name = models.CharField(max_length=100, help_text="心理師姓名")
    title = models.CharField(max_length=100, help_text="心理師頭銜，例如：諮商所督導")
    license_number = models.CharField(max_length=50, help_text="證照編號（如：諮心字第000485號）")
    education = models.TextField(help_text="學歷與證書")
    experience = models.TextField(help_text="經歷描述")
    specialties = models.TextField(help_text="專長描述（理論取向／服務對象）")
    beliefs = models.TextField(help_text="個人信念／諮商理念")
    publications = models.JSONField(default=list, help_text="文章列表（字串陣列）")
    photo = models.ImageField(upload_to='therapists/', null=True, blank=True, help_text="心理師頭像照片")
    created_at = models.DateTimeField(auto_now_add=True, help_text="建立時間")

     # 新增：諮詢模式（multi-select）
    CONSULTATION_CHOICES = [
        ('online', '線上'),
        ('offline', '實體'),
    ]
    consultation_modes = models.JSONField(
        default=list,
        help_text="可提供諮詢模式列表，範例：['online','offline']"
    )

    # 新增：收費資訊
    pricing = models.JSONField(
        default=dict,
        help_text="各模式收費，範例：{'online':2000,'offline':3000}"
    )

    # … __str__, Meta, etc. …
    def __str__(self):
        return self.name

class AvailableTime(models.Model):
    """
    心理師可預約時段，週期性設定（每週某日的某時段）。
    """
    WEEK_DAYS = [
        ('monday',   '週一'),
        ('tuesday',  '週二'),
        ('wednesday','週三'),
        ('thursday', '週四'),
        ('friday',   '週五'),
        ('saturday', '週六'),
        ('sunday',   '週日'),
    ]
    therapist = models.ForeignKey(
        TherapistProfile,
        related_name='available_times',
        on_delete=models.CASCADE,
        help_text="所屬心理師"
    )
    day_of_week = models.CharField(max_length=9, choices=WEEK_DAYS, help_text="星期幾")
    start_time = models.TimeField(help_text="開始時間")
    end_time = models.TimeField(help_text="結束時間")

    class Meta:
        ordering = ['therapist', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.therapist.name} — {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"

class AvailableSlot(models.Model):
    therapist = models.ForeignKey(TherapistProfile, on_delete=models.CASCADE)
    slot_time = models.DateTimeField()

    def __str__(self):
        return f"Slot for {self.therapist} at {self.slot_time}"