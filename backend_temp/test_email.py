#!/usr/bin/env python
"""
測試郵件通知功能的獨立腳本
"""
import os
import django
from django.conf import settings

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from appointments.models import Appointment
from appointments.notifications import send_appointment_created_notification, send_appointment_user_confirmation

def test_email_notifications():
    """測試郵件通知功能"""
    print("🧪 開始測試郵件通知功能...")
    
    # 獲取最新的預約
    try:
        latest_appointment = Appointment.objects.latest('created_at')
        print(f"📋 找到最新預約: ID {latest_appointment.id}")
        print(f"   - 用戶: {latest_appointment.user.email}")
        print(f"   - 狀態: {latest_appointment.status}")
        
        # 測試管理員通知
        print("\n📧 測試管理員通知...")
        admin_result = send_appointment_created_notification(latest_appointment)
        print(f"   - 管理員通知結果: {'✅ 成功' if admin_result else '❌ 失敗'}")
        
        # 測試用戶確認通知
        print("\n📧 測試用戶確認通知...")
        user_result = send_appointment_user_confirmation(latest_appointment)
        print(f"   - 用戶確認通知結果: {'✅ 成功' if user_result else '❌ 失敗'}")
        
        print(f"\n✅ 測試完成！")
        print(f"📨 郵件後端設定: {settings.EMAIL_BACKEND}")
        print(f"📤 預設發件人: {settings.DEFAULT_FROM_EMAIL}")
        print(f"👥 管理員信箱: {settings.ADMIN_EMAIL}")
        
    except Appointment.DoesNotExist:
        print("❌ 沒有找到預約記錄，請先創建一個預約")
    except Exception as e:
        print(f"❌ 測試過程發生錯誤: {e}")

if __name__ == "__main__":
    test_email_notifications()