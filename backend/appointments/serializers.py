# 導入Django用戶模型獲取函數
from django.contrib.auth import get_user_model
# 導入DRF序列化器
from rest_framework import serializers
# 導入心理師相關模型
from therapists.models import AvailableSlot, TherapistProfile
# 導入預約相關模型
from .models import Appointment, PreferredPeriod, AppointmentDetail
# 導入雜湊功能（用於身分證加密）
import hashlib

User = get_user_model()

class PreferredPeriodSerializer(serializers.ModelSerializer):
    """偏好時間段的序列化器"""
    period_display = serializers.SerializerMethodField()
    
    class Meta:
        model = PreferredPeriod
        fields = ['id', 'date', 'period', 'period_display']
    
    def get_period_display(self, obj):
        """獲取時段的中文顯示"""
        period_choices = {
            'morning': '上午 (09:00-12:00)',
            'afternoon': '下午 (13:00-17:00)', 
            'evening': '晚上 (18:00-21:00)'
        }
        return period_choices.get(obj.period, obj.period)

class AppointmentDetailSerializer(serializers.ModelSerializer):
    """預約詳細資訊的序列化器"""
    
    class Meta:
        model = AppointmentDetail
        fields = [
            'name', 'phone', 'main_concerns', 'previous_therapy',
            'urgency', 'special_needs', 'specialty_requested'
        ]

class AvailableSlotSerializer(serializers.ModelSerializer):
    """可用時段的序列化器"""
    
    class Meta:
        model = AvailableSlot
        fields = ['id', 'slot_time']

class AppointmentSerializer(serializers.ModelSerializer):
    # 基本欄位的只讀設定
    slot = AvailableSlotSerializer(read_only=True)  # 返回時段詳細資訊而非只有ID
    user = serializers.ReadOnlyField(source='user.email')  # 返回用戶Email
    therapist = serializers.SerializerMethodField()  # 返回心理師姓名（處理None情況）
    
    # 新增欄位：偏好時間段列表
    preferred_periods = PreferredPeriodSerializer(many=True, read_only=True)
    
    # 新增欄位：預約詳細資訊
    detail = AppointmentDetailSerializer(read_only=True)
    
    # 新增欄位：確認時間（從slot中獲取）
    confirmed_datetime = serializers.SerializerMethodField()
    
    # 新增欄位：諮商方式的中文顯示
    consultation_type_display = serializers.SerializerMethodField()
    
    # 新增欄位：狀態的中文顯示
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'therapist', 'slot',
            'consultation_type', 'consultation_type_display',
            'price', 'status', 'status_display',
            'created_at', 'confirmed_at',
            'confirmed_datetime', 'preferred_periods', 'detail'
        ]
        read_only_fields = fields
    
    def get_therapist(self, obj):
        """獲取心理師姓名"""
        return obj.therapist.name if obj.therapist else '待分配'
    
    def get_confirmed_datetime(self, obj):
        """獲取確認的具體時間"""
        # 如果有關聯的時段，返回時段時間
        if obj.slot and obj.slot.slot_time:
            return obj.slot.slot_time
        return None
    
    def get_consultation_type_display(self, obj):
        """獲取諮商方式的中文顯示"""
        type_choices = {
            'online': '線上諮商',
            'offline': '實體諮商'
        }
        return type_choices.get(obj.consultation_type, obj.consultation_type)
    
    def get_status_display(self, obj):
        """獲取狀態的中文顯示"""
        status_choices = {
            'pending': '待確認',
            'confirmed': '已確認',  
            'completed': '已完成',
            'cancelled': '已取消',
            'rejected': '已拒絕'
        }
        return status_choices.get(obj.status, obj.status)

class AppointmentCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        write_only=True,
        help_text='用戶電子郵件，作為帳號唯一識別'
    )
    id_number = serializers.CharField(
        write_only=True,
        help_text='用戶身分證號，後端雜湊比對'
    )
    slot = serializers.PrimaryKeyRelatedField(
        queryset=AvailableSlot.objects.filter(is_booked=False),
        required=False,
        help_text='要預約的 AvailableSlot id，且該時段尚未被預約'
    )
    consultation_type = serializers.ChoiceField(
        choices=Appointment.CONSULTATION_CHOICES,
        help_text='諮詢方式：online 或 offline'
    )
    
    # 新增前端發送的欄位
    therapist = serializers.PrimaryKeyRelatedField(
        queryset=TherapistProfile.objects.all(),
        required=False,
        help_text='指定的心理師ID'
    )
    specialty = serializers.IntegerField(
        write_only=True,
        required=False,
        help_text='專業領域ID'
    )
    preferred_periods = serializers.JSONField(
        write_only=True,
        required=False,
        help_text='偏好時間段'
    )
    name = serializers.CharField(
        write_only=True,
        required=True,
        help_text='用戶姓名'
    )
    phone = serializers.CharField(
        write_only=True,
        required=True,
        help_text='聯絡電話'
    )
    main_concerns = serializers.CharField(
        write_only=True,
        required=True,
        help_text='主要關注議題'
    )
    previous_therapy = serializers.BooleanField(
        write_only=True,
        required=False,
        help_text='是否曾接受過心理諮商'
    )
    urgency = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        allow_null=True,
        default='medium',
        help_text='緊急程度'
    )
    special_needs = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        allow_null=True,
        default='',
        help_text='特殊需求'
    )

    class Meta:
        model = Appointment
        fields = [
            'email', 'id_number', 'slot', 'consultation_type',
            'therapist', 'specialty', 'preferred_periods', 
            'name', 'phone', 'main_concerns', 'previous_therapy',
            'urgency', 'special_needs'
        ]

    def create(self, validated_data):
        email = validated_data.pop('email')
        raw_id = validated_data.pop('id_number')
        
        # 除錯：印出接收到的資料
        print(f"DEBUG: 建立預約 - Email: {email}, ID: {raw_id}")
        
        # 移除不屬於 Appointment 模型的欄位，但保留以備後用
        therapist_id = validated_data.pop('therapist', None)
        specialty = validated_data.pop('specialty', None)
        preferred_periods = validated_data.pop('preferred_periods', None)
        name = validated_data.pop('name', None)
        phone = validated_data.pop('phone', None)
        main_concerns = validated_data.pop('main_concerns', None)
        previous_therapy = validated_data.pop('previous_therapy', None)
        urgency = validated_data.pop('urgency', None)
        special_needs = validated_data.pop('special_needs', None)

        try:
            user = User.objects.get(email=email)
            print(f"DEBUG: 用戶已存在，驗證身分證...")
            if not user.check_id_number(raw_id):
                print(f"DEBUG: 身分證驗證失敗")
                raise serializers.ValidationError({'id_number': '身分證號不符 (建立預約時驗證失敗)'})
            print(f"DEBUG: 身分證驗證成功")
        except User.DoesNotExist:
            print(f"DEBUG: 用戶不存在，建立新用戶...")
            user = User(username=email, email=email)
            user.set_unusable_password()
            user.set_id_number(raw_id)
            user.save()
            print(f"DEBUG: 新用戶建立成功")

        # 如果指定了 therapist 但沒有 slot，將 therapist 設置到 appointment
        if therapist_id and not validated_data.get('slot'):
            validated_data['therapist'] = therapist_id
        elif validated_data.get('slot'):
            # 如果有指定 slot，從 slot 獲取 therapist
            validated_data['therapist'] = validated_data['slot'].therapist

        # 如果都沒有指定，預約狀態設為pending，由管理員後續分配心理師
        # 這符合「預約即註冊」的流程設計，用戶可以不指定特定心理師

        appointment = Appointment.objects.create(user=user, **validated_data)
        
        # 創建預約詳細資訊
        AppointmentDetail.objects.create(
            appointment=appointment,
            name=name or '',
            phone=phone or '',
            main_concerns=main_concerns or '',
            previous_therapy=previous_therapy or False,
            urgency=urgency or 'medium',
            special_needs=special_needs or '',
            specialty_requested=specialty
        )
        
        # 創建偏好時間記錄
        if preferred_periods:
            for period_data in preferred_periods:
                date = period_data.get('date')
                periods = period_data.get('periods', [])
                
                if date and periods:
                    for period in periods:
                        PreferredPeriod.objects.create(
                            appointment=appointment,
                            date=date,
                            period=period
                        )
        
        # 發送郵件通知
        from .notifications import send_appointment_created_notification, send_appointment_user_confirmation
        try:
            # 發送給管理員/心理師
            send_appointment_created_notification(appointment)
            # 發送確認郵件給用戶
            send_appointment_user_confirmation(appointment)
        except Exception as e:
            print(f"郵件通知發送失敗: {e}")
        
        return appointment
