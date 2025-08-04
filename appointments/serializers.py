from django.contrib.auth import get_user_model
from rest_framework import serializers
from therapists.models import AvailableSlot
from .models import Appointment
import hashlib

User = get_user_model()

class AppointmentSerializer(serializers.ModelSerializer):
    slot = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.ReadOnlyField(source='user.email')
    therapist = serializers.ReadOnlyField(source='therapist.name')

    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'therapist', 'slot',
            'consultation_type', 'price',
            'status', 'created_at'
        ]
        read_only_fields = fields

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
        help_text='要預約的 AvailableSlot id，且該時段尚未被預約'
    )
    consultation_type = serializers.ChoiceField(
        choices=Appointment.CONSULTATION_CHOICES,
        help_text='諮詢方式：online 或 offline'
    )

    class Meta:
        model = Appointment
        fields = ['email', 'id_number', 'slot', 'consultation_type']

    def create(self, validated_data):
        email = validated_data.pop('email')
        raw_id = validated_data.pop('id_number')

        try:
            user = User.objects.get(email=email)
            if not user.check_id_number(raw_id):
                raise serializers.ValidationError({'id_number': '身分證號不符'})
        except User.DoesNotExist:
            user = User(username=email, email=email)
            user.set_unusable_password()
            user.set_id_number(raw_id)
            user.save()

        appointment = Appointment.objects.create(user=user, **validated_data)
        return appointment
