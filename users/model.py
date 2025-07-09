import hashlib
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(AbstractUser):
    """
    自訂使用者模型：
    - email 作為唯一識別
    - id_number_hash 儲存 SHA256 salted hash of ID number
    """
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', '男性'), ('female', '女性'), ('other', '其他')],
        blank=True
    )
    birthday = models.DateField(null=True, blank=True)

    # 新增：身分證雜湊欄位
    id_number_hash = models.CharField(
        max_length=128,
        blank=True,
        help_text="SHA256 salted hash of ID number"
    )

    def set_id_number(self, raw_id: str):
        """設定身分證雜湊值（只呼叫一次或更新時）"""
        # make_password 內會自動加 salt
        self.id_number_hash = make_password(raw_id)

    def check_id_number(self, raw_id: str) -> bool:
        """驗證輸入的身分證是否正確"""
        return check_password(raw_id, self.id_number_hash)

    def __str__(self):
        return self.email
