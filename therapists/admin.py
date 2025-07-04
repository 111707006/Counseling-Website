from django.contrib import admin
from .models import TherapistProfile, AvailableTime

class AvailableTimeInline(admin.TabularInline):
    model = AvailableTime
    extra = 1
    fields = ('day_of_week', 'start_time', 'end_time')
    verbose_name = "可預約時段"
    verbose_name_plural = "可預約時段"

@admin.register(TherapistProfile)
class TherapistProfileAdmin(admin.ModelAdmin):
    # 將 consultation_modes 與 pricing 加入列表頁顯示
    list_display = (
        'name', 'title', 'license_number',
        'get_consultation_modes', 'get_pricing_summary', 'created_at'
    )
    # 可以用 consultation_modes 來過濾
    list_filter = ('consultation_modes',)
    search_fields = ('name', 'title', 'license_number')
    inlines = [AvailableTimeInline]

    # 分組顯示欄位：基本資料 + 服務設定
    fieldsets = (
        (None, {
            'fields': (
                'name', 'title', 'license_number',
                'education', 'experience',
                'specialties', 'beliefs', 'publications', 'photo'
            )
        }),
        ('服務設定', {
            'fields': ('consultation_modes', 'pricing')
        }),
    )

    def get_consultation_modes(self, obj):
        # 將 list 轉成逗號分隔字串
        return ", ".join(obj.consultation_modes)
    get_consultation_modes.short_description = "諮詢模式"

    def get_pricing_summary(self, obj):
        # 簡要顯示 pricing dict
        return "; ".join(f"{mode}: {price}" for mode, price in obj.pricing.items())
    get_pricing_summary.short_description = "收費資訊"

@admin.register(AvailableTime)
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    search_fields = ('therapist__name',)
