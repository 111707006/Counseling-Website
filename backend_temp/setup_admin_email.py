#!/usr/bin/env python
"""
設定管理員帳號並測試郵件發送功能
"""
import os
import django
from django.conf import settings

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction

User = get_user_model()

def create_admin_user():
    """創建新的管理員用戶"""
    email = 'tpeap01@cyc.tw'
    password = 'admin123456'
    
    print("🔧 創建管理員帳號...")
    print(f"📧 Email: {email}")
    print(f"🔑 密碼: {password}")
    
    try:
        with transaction.atomic():
            # 檢查是否已存在
            if User.objects.filter(email=email).exists():
                print(f"⚠️  管理員 {email} 已存在，更新權限...")
                admin_user = User.objects.get(email=email)
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.save()
            else:
                # 創建管理員用戶
                admin_user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    is_staff=True,
                    is_superuser=True
                )
                print(f"✅ 成功創建管理員: {email}")
                
            return admin_user
            
    except Exception as e:
        print(f"❌ 創建管理員失敗: {e}")
        return None

def test_email_settings():
    """測試郵件設定"""
    print("\n📋 檢查郵件設定...")
    print(f"📤 EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"🏢 EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"🔌 EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"🔒 EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"👤 EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"🔑 EMAIL_HOST_PASSWORD: {'已設定' if settings.EMAIL_HOST_PASSWORD else '未設定'}")
    print(f"📧 DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"👑 ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
    
    # 檢查必要設定
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("\n⚠️  警告：EMAIL_HOST_USER 或 EMAIL_HOST_PASSWORD 未設定")
        print("📝 請在 .env 檔案中設定：")
        print("   EMAIL_HOST_USER=你的Gmail帳號@gmail.com")
        print("   EMAIL_HOST_PASSWORD=你的Gmail應用程式密碼")
        return False
    
    return True

def send_test_email():
    """發送測試郵件"""
    print("\n📨 發送測試郵件...")
    
    try:
        subject = '🎉 心理諮商系統管理員帳號設定完成'
        message = f"""
親愛的管理員，

恭喜！您的心理諮商系統管理員帳號已成功設定。

📋 帳號資訊：
- 管理後台：http://localhost:8000/admin/
- 帳號：tpeap01@cyc.tw
- 密碼：admin123456

🔧 系統功能：
- ✅ 預約管理：處理用戶預約申請
- ✅ 心理師管理：維護心理師資料
- ✅ 測驗管理：查看心理測驗結果
- ✅ 文章管理：發布心理健康文章
- ✅ 郵件通知：自動發送預約通知

📧 郵件通知測試：
如果您收到這封郵件，表示郵件系統已正常運作！

系統會在以下情況自動發送郵件：
- 用戶提交新預約申請時
- 預約狀態變更時
- 系統重要通知時

祝您使用愉快！

💝 心理諮商系統
        """
        
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        if result:
            print(f"✅ 測試郵件已發送到：{settings.ADMIN_EMAIL}")
            print("📬 請檢查您的收件匣（包含垃圾郵件匣）")
            return True
        else:
            print("❌ 郵件發送失敗")
            return False
            
    except Exception as e:
        print(f"❌ 郵件發送錯誤：{e}")
        print("\n💡 可能的解決方案：")
        print("1. 檢查 Gmail 帳號和應用程式密碼是否正確")
        print("2. 確認 Gmail 已開啟「二步驟驗證」")
        print("3. 確認已產生「應用程式密碼」")
        print("4. 檢查網路連線")
        return False

def main():
    """主函數"""
    print("🚀 開始設定管理員帳號和郵件系統...")
    print("=" * 60)
    
    # 1. 創建管理員
    admin_user = create_admin_user()
    if not admin_user:
        return
    
    # 2. 檢查郵件設定
    if not test_email_settings():
        print("\n❌ 郵件設定不完整，無法發送測試郵件")
        print("📝 請先設定 .env 檔案中的 EMAIL_HOST_USER 和 EMAIL_HOST_PASSWORD")
        return
    
    # 3. 發送測試郵件
    success = send_test_email()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 設定完成！")
        print(f"🔗 管理後台：http://localhost:8000/admin/")
        print(f"📧 管理員帳號：tpeap01@cyc.tw")
        print(f"🔑 管理員密碼：admin123456")
    else:
        print("⚠️  管理員帳號已創建，但郵件發送失敗")
        print("請檢查 SMTP 設定後重新測試")

if __name__ == "__main__":
    main()