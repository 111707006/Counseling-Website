#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def check_admin_access():
    print("檢查 Admin 訪問...")
    
    # 創建測試客戶端
    client = Client()
    
    # 嘗試訪問 admin 主頁
    response = client.get('/admin/')
    print(f"Admin 主頁狀態碼: {response.status_code}")
    
    # 登入管理員
    admin_user = User.objects.filter(email='admin@mindcare.com').first()
    if admin_user:
        login_success = client.login(username='admin@mindcare.com', password='admin123456')
        print(f"管理員登入成功: {login_success}")
        
        if login_success:
            # 再次訪問 admin 主頁
            response = client.get('/admin/')
            print(f"登入後 Admin 主頁狀態碼: {response.status_code}")
            
            # 檢查是否包含 appointments
            content = response.content.decode('utf-8')
            if 'appointments' in content.lower():
                print("OK - Admin 頁面包含 appointments")
            else:
                print("ERROR - Admin 頁面不包含 appointments")
                print("頁面內容片段:")
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'model' in line.lower() or 'app' in line.lower():
                        print(f"  {i}: {line.strip()[:100]}")
            
            # 嘗試訪問 appointments 管理頁面
            try:
                appointments_url = '/admin/appointments/appointment/'
                response = client.get(appointments_url)
                print(f"Appointments 管理頁面狀態碼: {response.status_code}")
                
                if response.status_code == 200:
                    print("OK - 可以訪問 Appointments 管理頁面")
                else:
                    print("ERROR - 無法訪問 Appointments 管理頁面")
                    
            except Exception as e:
                print(f"訪問 Appointments 頁面時錯誤: {e}")
    else:
        print("ERROR - 未找到管理員用戶")

if __name__ == "__main__":
    check_admin_access()