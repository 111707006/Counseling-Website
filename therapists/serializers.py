from rest_framework import serializers
from .models import TherapistProfile, AvailableTime

class AvailableTimeSerializer(serializers.ModelSerializer):
    """
    將心理師時段設定轉為 JSON。
    """
    class Meta:
        model = AvailableTime
        fields = ('id', 'day_of_week', 'start_time', 'end_time')

class TherapistProfileSerializer(serializers.ModelSerializer):
    """
    將心理師個人簡介與時段設定轉為 JSON，提供前台讀取。
    """
    available_times = AvailableTimeSerializer(many=True, read_only=True)

    class Meta:
         model = TherapistProfile
         fields = (
            'id', 'name', 'title', 'license_number', 'education', 'experience',
            'specialties', 'beliefs', 'publications', 'photo',
            'available_times',  # ← 修正：加逗號
            'consultation_modes',
            'pricing',
            'created_at',       # ← 新增：註冊／建立時間
        )
