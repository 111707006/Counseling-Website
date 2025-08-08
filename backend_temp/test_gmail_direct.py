#!/usr/bin/env python3
"""
直接測試Gmail SMTP設定
"""
import os
import django
from pathlib import Path

# 設定Django環境
import sys
sys.path.append(str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_gmail_direct():
    """直接測試Gmail SMTP發送"""
    try:
        print("=== Gmail SMTP 設定測試 ===")
        print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        print()
        
        # 測試發送郵件
        result = send_mail(
            subject='Gmail SMTP 測試郵件',
            message='這是一封測試郵件，用於驗證Gmail SMTP設定是否正常運作。',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['tpeap01@cyc.tw'],  # 發送給自己測試
            fail_silently=False,
        )
        
        print(f"Gmail mail sent successfully! send_mail result: {result}")
        print("Please check your Gmail inbox!")
        return True
        
    except Exception as e:
        print(f"Gmail mail sending failed: {e}")
        return False

if __name__ == "__main__":
    test_gmail_direct()