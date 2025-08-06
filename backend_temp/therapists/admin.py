from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from .models import TherapistProfile, AvailableTime, Specialty

User = get_user_model()

class TherapistProfileForm(forms.ModelForm):
    """自定義心理師表單，支援直接輸入 email 創建用戶"""
    
    user_email = forms.EmailField(
        label="用戶 Email",
        required=False,
        help_text="輸入 email 地址，如果用戶不存在將自動創建。留空則不關聯任何用戶。"
    )
    
    class Meta:
        model = TherapistProfile
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),  # 隱藏原來的 user 選擇欄位
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 如果是編輯模式且已有關聯用戶，預填 email
        if self.instance.pk and self.instance.user:
            self.fields['user_email'].initial = self.instance.user.email
    
    def clean_user_email(self):
        email = self.cleaned_data.get('user_email')
        if not email:
            return email
            
        # 檢查 email 格式
        if email and '@' not in email:
            raise ValidationError("請輸入有效的 email 地址")
        
        return email
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        email = self.cleaned_data.get('user_email')
        
        if email:
            # 嘗試獲取或創建用戶
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,  # 使用 email 作為 username
                    'is_active': True,
                }
            )
            
            # 如果是新創建的用戶，設置一個臨時密碼
            if created:
                # 生成隨機密碼
                import secrets
                import string
                password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                user.set_password(password)
                user.save()
            
            instance.user = user
        else:
            # 如果沒有提供 email，清除用戶關聯
            instance.user = None
        
        if commit:
            instance.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()
        
        return instance

class AvailableTimeInline(admin.TabularInline):
    model = AvailableTime
    extra = 1
    fields = ('day_of_week', 'start_time', 'end_time')
    verbose_name = "可預約時段"
    verbose_name_plural = "可預約時段"

@admin.register(TherapistProfile)
class TherapistProfileAdmin(admin.ModelAdmin):
    form = TherapistProfileForm  # 使用自定義表單
    
    list_display = (
        'name', 'title', 'license_number', 'get_user_email',
        'get_consultation_modes', 'created_at'
    )
    list_filter = ('consultation_modes', 'specialties')
    search_fields = ('name', 'specialties__name', 'specialties_text', 'license_number', 'user__email')
    ordering = ('-created_at',)
    inlines = [AvailableTimeInline]

    fieldsets = (
        ('基本資訊', {
            'fields': (
                'user_email',  # 使用自定義的 email 欄位
                'name', 'title', 'license_number',
                'education', 'experience', 'beliefs', 
                'photo'
            )
        }),
        ('專業領域', {
            'fields': ('specialties', 'specialties_text'),
            'description': '新的關聯式專業領域和舊的文字描述（過渡期保留）'
        }),
        ('服務設定', {
            'fields': ('consultation_modes',)
        }),
    )
    
    filter_horizontal = ('specialties',)  # 讓專業領域選擇更友善

    def get_user_email(self, obj):
        """顯示關聯用戶的 email"""
        if obj.user:
            return obj.user.email
        return "未關聯用戶"
    get_user_email.short_description = "用戶 Email"

    def get_consultation_modes(self, obj):
        return ", ".join(obj.consultation_modes)
    get_consultation_modes.short_description = "諮詢模式"

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


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_therapists_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active')
        }),
    )
    
    def get_therapists_count(self, obj):
        return obj.therapists.count()
    get_therapists_count.short_description = "使用療師數量"
