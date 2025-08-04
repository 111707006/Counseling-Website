#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.contrib.auth import get_user_model
from appointments.models import Appointment
from django.contrib import admin

User = get_user_model()

def simple_admin_test():
    print("=" * 50)
    print("Django 管理後台檢查")
    print("=" * 50)
    
    # 1. 檢查管理員
    admin_count = User.objects.filter(is_staff=True).count()
    print(f"管理員數量: {admin_count}")
    
    # 2. 檢查預約數據
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    print(f"總預約數: {total_appointments}")
    print(f"待處理預約: {pending_appointments}")
    
    # 3. 檢查 Admin 註冊
    appointment_registered = Appointment in admin.site._registry
    print(f"Appointment 已註冊: {appointment_registered}")
    
    # 4. 檢查模板
    import os
    templates_exist = os.path.exists('templates/admin/appointments')
    print(f"模板目錄存在: {templates_exist}")
    
    print("\n" + "=" * 50)
    print("測試結果:")
    
    all_good = (
        admin_count > 0 and 
        appointment_registered and 
        templates_exist
    )
    
    if all_good:
        print("OK - 系統可以正常使用")
        print("\n登入資訊:")
        print("地址: http://localhost:8000/admin/")
        print("帳號: admin@mindcare.com") 
        print("密碼: admin123456")
        
        if pending_appointments > 0:
            print(f"\n注意: 有 {pending_appointments} 筆預約待處理")
            
    else:
        print("ERROR - 系統有問題")
    
    print("=" * 50)

if __name__ == "__main__":
    simple_admin_test()