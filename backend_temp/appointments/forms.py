from django import forms
from .models import Appointment


class AppointmentAdminForm(forms.ModelForm):
    """預約管理表單"""
    
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'admin_notes': forms.Textarea(attrs={
                'rows': 4, 
                'cols': 60,
                'placeholder': '管理員備註：可記錄特殊事項、提醒事項等...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 根據諮商類型動態調整諮商室選項
        if self.instance and hasattr(self.instance, 'consultation_type'):
            consultation_type = self.instance.consultation_type
            
            # 線上諮商只顯示線上會議室選項
            if consultation_type == 'online':
                self.fields['consultation_room'].choices = [
                    ('', '---------'),
                    ('online_room', '線上會議室'),
                ]
            # 實體諮商顯示實體諮商室選項
            elif consultation_type == 'offline':
                self.fields['consultation_room'].choices = [
                    ('', '---------'),
                    ('room_2', '諮商室 2'),
                    ('room_3', '諮商室 3'),
                    ('room_4', '諮商室 4'),
                    ('room_5', '諮商室 5'),
                ]
        
        # 為諮商室欄位添加幫助文字
        self.fields['consultation_room'].help_text = '根據諮商方式選擇合適的諮商室'
        
        # 設定備註欄位的標籤和幫助文字
        self.fields['admin_notes'].label = '管理員備註'
        self.fields['admin_notes'].help_text = '此備註僅管理員可見，用於記錄特殊事項、提醒等'