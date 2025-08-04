from django.contrib import admin
from .models import TherapistProfile, AvailableTime, Specialty, SpecialtyCategory

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
    list_filter = ('consultation_modes', 'specialties')
    search_fields = ('name', 'specialties__name', 'specialties_text', 'license_number')
    ordering = ('-created_at',)
    inlines = [AvailableTimeInline]

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'name', 'title', 'license_number',
                'education', 'experience', 'beliefs', 
                'publications', 'photo'
            )
        }),
        ('專業領域', {
            'fields': ('specialties', 'specialties_text'),
            'description': '新的關聯式專業領域和舊的文字描述（過渡期保留）'
        }),
        ('服務設定', {
            'fields': ('consultation_modes', 'pricing')
        }),
    )
    
    filter_horizontal = ('specialties',)  # 讓專業領域選擇更友善

    def get_consultation_modes(self, obj):
        return ", ".join(obj.consultation_modes)
    get_consultation_modes.short_description = "諮詢模式"

    def get_pricing_summary(self, obj):
        return "; ".join(f"{mode}: {price}" for mode, price in obj.pricing.items())
    get_pricing_summary.short_description = "收費資訊"

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
    autocomplete_fields = ('therapist',)  # 讓可預約時段更方便地選擇心理師


@admin.register(SpecialtyCategory)
class SpecialtyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_specialties_count', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    def get_specialties_count(self, obj):
        return obj.specialties.count()
    get_specialties_count.short_description = "專業領域數量"


class SpecialtyInline(admin.TabularInline):
    model = Specialty
    extra = 1
    fields = ('name', 'description', 'is_active')


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_therapists_count', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    ordering = ('category__name', 'name')
    list_select_related = ('category',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description', 'is_active')
        }),
    )
    
    def get_therapists_count(self, obj):
        return obj.therapists.count()
    get_therapists_count.short_description = "使用療師數量"


# 在 SpecialtyCategoryAdmin 中加入 inline
SpecialtyCategoryAdmin.inlines = [SpecialtyInline]
