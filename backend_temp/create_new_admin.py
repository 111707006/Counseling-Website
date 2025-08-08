#!/usr/bin/env python
import os
import sys
import django
from django.contrib.auth.hashers import make_password

# 設置 Django 環境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from users.models import User

def create_new_admin():
    print("創建新的管理員帳號...")
    
    # 新管理員資料
    admin_data = {
        'email': 'manager@mindcare.com',
        'username': 'manager',
        'first_name': '系統',
        'last_name': '管理員',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    }
    
    password = 'Manager2025!'
    
    # 檢查是否已存在
    if User.objects.filter(email=admin_data['email']).exists():
        print(f"帳號 {admin_data['email']} 已存在")
        existing_user = User.objects.get(email=admin_data['email'])
        existing_user.set_password(password)
        existing_user.save()
        print("密碼已重設")
    else:
        # 創建新用戶
        admin_user = User.objects.create(**admin_data)
        admin_user.set_password(password)
        admin_user.save()
        print(f"成功創建新管理員帳號")
    
    print("\n" + "="*50)
    print("新管理員帳號資訊")
    print("="*50)
    print(f"後台網址: http://localhost:8000/admin/")
    print(f"帳號 (Email): {admin_data['email']}")
    print(f"密碼: {password}")
    print(f"用戶名: {admin_data['username']}")
    print(f"顯示名稱: {admin_data['first_name']} {admin_data['last_name']}")
    print("="*50)
    print("權限:")
    print("超級管理員權限 (superuser)")
    print("員工權限 (staff)")
    print("帳號已啟用 (active)")
    print("="*50)
    
    # 顯示所有管理員帳號
    print("\n所有管理員帳號:")
    admins = User.objects.filter(is_staff=True, is_superuser=True)
    for i, admin in enumerate(admins, 1):
        status = "啟用" if admin.is_active else "停用"
        print(f"{i}. {admin.email} ({admin.username}) - {status}")

if __name__ == '__main__':
    create_new_admin()