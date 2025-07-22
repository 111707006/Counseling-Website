# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from .models import Appointment
# from therapists.models import AvailableSlot

# User = get_user_model()

# class AppointmentSerializer(serializers.ModelSerializer):
#     """供查詢用：返回完整預約資料（不含敏感 id_number）"""
#     user_email = serializers.ReadOnlyField(source='user.email')
#     user_id = serializers.ReadOnlyField(source='user.id')

#     class Meta:
#         model = Appointment
#         fields = (
#             'id', 'user_id', 'user_email', 'therapist',
#             'slot', 'consultation_type', 'price',
#             'status', 'created_at'
#         )
#         read_only_fields = fields

# class AppointmentCreateSerializer(serializers.ModelSerializer):
#     """
#     建立預約時同時處理「預約即註冊」：
#     - 輸入 email + id_number
#     - 若用戶不存在，建立一筆 User 並 set_id_number
#     - 若已存在，驗證 id_number 正確才繼續
#     """
#     email = serializers.EmailField(write_only=True)
#     id_number = serializers.CharField(write_only=True)
#     slot = serializers.PrimaryKeyRelatedField(
#         queryset=AvailableSlot.objects.filter(is_booked=False),
#         help_text='要預約的 AvailableSlot id，且該時段尚未被預約'
#     )

#     class Meta:
#         model = Appointment
#         fields = ['email', 'id_number', 'slot', 'consultation_type']

#     def validate(self, attrs):
#         email = attrs.get('email')
#         id_number = attrs.get('id_number')
#         user_qs = User.objects.filter(email=email)
#         if user_qs.exists():
#             user = user_qs.first()
#             if not user.check_id_number(id_number):
#                 raise serializers.ValidationError("身分證號驗證失敗")
#         return attrs

#     def create(self, validated_data):
#         email = validated_data.pop('email')
#         id_number = validated_data.pop('id_number')
#         # 取得或建立 user
#         user, created = User.objects.get_or_create(
#             email=email,
#             defaults={'username': email}
#         )
#         # 若是新 user，或 id_number_hash 不存在，設定身分證雜湊
#         if created or not user.check_id_number(id_number):
#             user.set_id_number(id_number)
#             user.save()
#         # 建立預約，perform_create 會自動計價並標記 slot
#         appointment = Appointment.objects.create(user=user, **validated_data)
#         return appointment
