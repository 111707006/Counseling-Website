from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    自訂使用者模型，繼承自 Django 內建 AbstractUser。
    新增 role 欄位：user / therapist / admin
    並強化 email 為唯一欄位。
    """
    ROLE_CHOICES = [
        ('user', '一般用戶'),
        ('therapist', '心理師'),
        ('admin', '管理員'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True, blank=False)


    def __str__(self):
        return f"{self.username} ({self.role})"
