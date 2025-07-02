from rest_framework import serializers
from .models import Appointment
from therapists.models import AvailableSlot

class SlotSerializer(serializers.ModelSerializer):
    """
    用於顯示心理師可預約時段
    """
    class Meta:
        model = AvailableSlot
        fields = ['id', 'start_time', 'end_time']

class AppointmentSerializer(serializers.ModelSerializer):
    """
    用於讀取預約紀錄的序列化器
    """
    slot = SlotSerializer(read_only=True)  # 顯示時段資訊
    class Meta:
        model = Appointment
        # 列出所有需要給前端的欄位
        fields = ['id', 'user', 'therapist', 'slot', 'consultation_type', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'therapist', 'slot', 'status', 'created_at']

class AppointmentCreateSerializer(serializers.ModelSerializer):
    """
    用於建立預約的序列化器
    前端只需提供 slot 與 consultation_type
    """
    slot = serializers.PrimaryKeyRelatedField(
        queryset=AvailableSlot.objects.filter(is_booked=False),
        help_text='要預約的 AvailableSlot id，且該時段尚未被預約'
    )
    consultation_type = serializers.ChoiceField(
        choices=Appointment.CONSULTATION_CHOICES,
        help_text='諮詢方式：online 或 offline'
    )

    class Meta:
        model = Appointment
        fields = ['slot', 'consultation_type']

    def validate(self, attrs):
        """
        確保前端不誤傳 therapist 等欄位
        """
        return attrs

    def create(self, validated_data):
        """
        建立預約並且鎖定時段（is_booked=True）
        """
        user = self.context['request'].user
        slot = validated_data['slot']
        # 將時段標記為已預約
        slot.is_booked = True
        slot.save()

        # 建立 Appointment，psychotherapist 與 user 由 slot 與 context 設定
        appointment = Appointment.objects.create(
            user=user,
            therapist=slot.therapist,
            slot=slot,
            consultation_type=validated_data['consultation_type']
        )
        return appointment
