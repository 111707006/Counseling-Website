from rest_framework import serializers
from .models import Appointment
from therapists.models import AvailableSlot

class AppointmentSerializer(serializers.ModelSerializer):
    slot = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
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
