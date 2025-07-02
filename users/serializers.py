# users/serializers.py

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    """
    註冊使用者時使用的序列化器
    - 驗證 email 唯一性
    - 驗證密碼強度
    - 阻擋使用者自行註冊為 admin
    """
    # 強制 email 唯一，並自訂錯誤訊息
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="此 Email 已被註冊"
            )
        ]
    )
    # 密碼只寫入，不回傳，並檢查強度
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    # 限定為模型中定義的三種角色
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default='user'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def validate_role(self, value):
        """
        阻止使用者註冊為管理員角色
        """
        if value == 'admin':
            raise serializers.ValidationError("無法自行註冊成管理員")
        return value

    def create(self, validated_data):
        """
        建立新使用者，使用 Django 內建的 create_user
        以確保密碼雜湊、安全性設定等都正確處理
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user
