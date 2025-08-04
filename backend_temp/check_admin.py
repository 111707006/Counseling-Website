#!/usr/bin/env python
"""
檢查管理員帳號資訊
"""
import os
import sys
import django

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def check_admin_users():
    print("🔍 檢查管理員帳號資訊...")
    print("=" * 50)
    
    # 查找所有管理員用戶
    admin_users = User.objects.filter(is_staff=True)
    
    if not admin_users.exists():
        print("❌ 未找到管理員帳號")
        print("\n建議執行以下命令創建管理員：")
        print("python manage.py create_admin")
        print("\n預設管理員資訊：")
        print("📧 Email: admin@mindcare.com")
        print("🔑 密碼: admin123456")
    else:
        print(f"✅ 找到 {admin_users.count()} 個管理員帳號:")
        print()
        
        for i, user in enumerate(admin_users, 1):
            print(f"管理員 {i}:")
            print(f"  📧 Email: {user.email}")
            print(f"  👤 用戶名: {user.username}")
            print(f"  🔒 超級用戶: {'是' if user.is_superuser else '否'}")
            print(f"  📅 創建時間: {user.date_joined.strftime('%Y-%m-%d %H:%M')}")
            print(f"  🔗 管理後台: http://localhost:8000/admin/")
            print()
    
    print("=" * 50)
    
    # 檢查系統狀態
    from appointments.models import Appointment
    from therapists.models import TherapistProfile
    
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    total_therapists = TherapistProfile.objects.count()
    
    print("📊 系統狀態:")
    print(f"  預約總數: {total_appointments}")
    print(f"  待處理預約: {pending_appointments}")
    print(f"  心理師總數: {total_therapists}")

if __name__ == "__main__":
    try:
        check_admin_users()
    except Exception as e:
        print(f"❌ 執行錯誤: {e}")