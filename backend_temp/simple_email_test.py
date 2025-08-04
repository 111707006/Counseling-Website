import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')

import django
django.setup()

from django.core.mail import send_mail
from django.conf import settings

# 簡單測試郵件發送
try:
    print("測試基本郵件發送...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    result = send_mail(
        subject='測試郵件',
        message='這是一個測試郵件',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['test@example.com'],
        fail_silently=False,
    )
    print(f"郵件發送結果: {result}")
    print("測試完成！")
    
except Exception as e:
    print(f"錯誤: {e}")