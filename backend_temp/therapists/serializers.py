from rest_framework import serializers
from .models import TherapistProfile, AvailableTime, Specialty, SpecialtyCategory


class SpecialtyCategorySerializer(serializers.ModelSerializer):
    """專業領域分類序列化器"""
    class Meta:
        model = SpecialtyCategory
        fields = ('id', 'name', 'description')


class SpecialtySerializer(serializers.ModelSerializer):
    """專業領域序列化器"""
    category = SpecialtyCategorySerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Specialty
        fields = ('id', 'name', 'category', 'category_name', 'description', 'is_active')


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
    user_id = serializers.ReadOnlyField(source='user.id')
    available_times = AvailableTimeSerializer(many=True, read_only=True)
    
    # 關聯式專業領域
    specialties = SpecialtySerializer(many=True, read_only=True)
    specialties_display = serializers.CharField(source='get_specialties_display', read_only=True)
    specialties_by_category = serializers.JSONField(source='get_specialties_by_category', read_only=True)
    
    # 向後相容：保留舊格式的專業領域文字
    specialties_text = serializers.CharField(read_only=True)

    class Meta:
         model = TherapistProfile
         fields = (
            'id','user_id', 'name', 'title', 'license_number', 'education', 'experience',
            'specialties',          # 新的關聯式專業領域
            'specialties_display',  # 顯示文字
            'specialties_by_category',  # 依分類整理
            'specialties_text',     # 舊格式（向後相容）
            'beliefs', 'publications', 'photo',
            'available_times',
            'consultation_modes',
            'pricing',
            'created_at',
        )
