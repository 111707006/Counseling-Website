from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    自訂使用者模型：移除 role 欄位，新增性別與生日欄位。
    """
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=[('male', '男性'), ('female', '女性'), ('other', '其他')], blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
