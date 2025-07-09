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
    list_display = (
        'name', 'title', 'license_number',
        'get_consultation_modes', 'get_pricing_summary', 'created_at'
    )
    list_filter = ('consultation_modes',)
    search_fields = ('name', 'specialties', 'license_number')
    ordering = ('-created_at',)
    inlines = [AvailableTimeInline]

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
        return ", ".join(obj.consultation_modes)
    get_consultation_modes.short_description = "諮詢模式"

    def get_pricing_summary(self, obj):
        return "; ".join(f"{mode}: {price}" for mode, price in obj.pricing.items())
    get_pricing_summary.short_description = "收費資訊"

    # 開啟 autocomplete 功能（沒有可用 FK，故移除錯誤設定）

@admin.register(AvailableTime)
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'day_of_week', 'start_time', 'end_time')
    list_filter = (
        'day_of_week',
        'therapist',            # 可以依心理師過濾
    )
    search_fields = (
        'therapist__name',      # 透過心理師姓名搜尋
    )
    ordering = (
        'therapist__name',
        'day_of_week',
        'start_time',
    )
    list_select_related = ('therapist',)  # 加快查 therapist 關聯

    # 若想透過 autocomplete 快速找心理師，可在 TherapistProfileAdmin 先設定:
    autocomplete_fields = ('therapist',)  # 讓可預約時段更便捷地選擇心理師
