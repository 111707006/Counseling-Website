#!/usr/bin/env python
"""
綜合系統測試腳本
檢查整個心理諮商系統的潛在問題
"""

import os
import sys
import django
import json
import requests
from datetime import datetime, timedelta

# 設置Django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.contrib.auth import get_user_model
from therapists.models import TherapistProfile, Specialty, AvailableSlot
from appointments.models import Appointment, PreferredPeriod, AppointmentDetail
from articles.models import Article
from assessments.models import Test, Question, Choice, Response

User = get_user_model()

class SystemTester:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3003"
        
    def log_error(self, test_name, message):
        self.errors.append(f"❌ {test_name}: {message}")
        print(f"❌ {test_name}: {message}")
        
    def log_warning(self, test_name, message):
        self.warnings.append(f"⚠️  {test_name}: {message}")
        print(f"⚠️  {test_name}: {message}")
        
    def log_pass(self, test_name, message=""):
        self.passed.append(f"✅ {test_name}: {message}")
        print(f"✅ {test_name}: {message}")

    def test_database_models(self):
        """測試資料庫模型完整性"""
        print("\n📊 測試資料庫模型...")
        
        # 測試User模型的身分證方法
        try:
            test_user = User(email="test@test.com", username="test@test.com")
            test_user.set_id_number("A123456789")
            if hasattr(test_user, 'check_id_number') and hasattr(test_user, 'set_id_number'):
                self.log_pass("User模型身分證方法", "set_id_number和check_id_number方法存在")
            else:
                self.log_error("User模型身分證方法", "缺少身分證相關方法")
        except Exception as e:
            self.log_error("User模型身分證方法", f"測試失敗: {e}")

        # 檢查TherapistProfile模型欄位
        try:
            profile_fields = [field.name for field in TherapistProfile._meta.fields]
            required_fields = ['name', 'title', 'license_number', 'education', 'experience', 'beliefs']
            missing_fields = [field for field in required_fields if field not in profile_fields]
            
            if missing_fields:
                self.log_error("TherapistProfile模型", f"缺少必要欄位: {missing_fields}")
            else:
                self.log_pass("TherapistProfile模型", "所有必要欄位存在")
                
            # 檢查是否有pricing欄位（不應該有）
            if 'pricing' in profile_fields:
                self.log_warning("TherapistProfile模型", "仍存在pricing欄位，前端已移除此功能")
                
        except Exception as e:
            self.log_error("TherapistProfile模型", f"檢查失敗: {e}")

        # 檢查Appointment模型關聯
        try:
            appointment_fields = [field.name for field in Appointment._meta.fields]
            required_relations = ['user', 'therapist', 'slot']
            
            for relation in required_relations:
                if relation in appointment_fields:
                    self.log_pass(f"Appointment.{relation}", "關聯欄位存在")
                else:
                    self.log_error(f"Appointment.{relation}", "關聯欄位缺失")
                    
        except Exception as e:
            self.log_error("Appointment模型關聯", f"檢查失敗: {e}")

    def test_api_endpoints(self):
        """測試API端點可用性"""
        print("\n🌐 測試API端點...")
        
        endpoints = [
            ("/api/therapists/profiles/", "GET", "心理師列表"),
            ("/api/therapists/specialties/", "GET", "專業領域列表"),
            ("/api/appointments/", "GET", "預約列表"),
            ("/api/articles/articles/", "GET", "文章列表"),
            ("/api/assessments/tests/", "GET", "測驗列表"),
        ]
        
        for endpoint, method, description in endpoints:
            try:
                url = f"{self.backend_url}{endpoint}"
                if method == "GET":
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        self.log_pass(f"API {description}", f"{endpoint} 回應正常")
                    elif response.status_code == 401:
                        self.log_warning(f"API {description}", f"{endpoint} 需要認證")
                    else:
                        self.log_error(f"API {description}", f"{endpoint} 回應碼: {response.status_code}")
                        
            except requests.exceptions.ConnectionError:
                self.log_error(f"API {description}", f"無法連接到 {url}")
            except Exception as e:
                self.log_error(f"API {description}", f"測試失敗: {e}")

    def test_appointment_creation(self):
        """測試預約建立流程"""
        print("\n📅 測試預約建立流程...")
        
        try:
            # 測試預約API
            appointment_data = {
                "email": "test_user@example.com",
                "id_number": "A123456789",
                "consultation_type": "offline",
                "name": "測試用戶",
                "phone": "0912345678",
                "main_concerns": "測試預約功能",
                "previous_therapy": False,
                "urgency": "medium",
                "special_needs": ""
            }
            
            url = f"{self.backend_url}/api/appointments/"
            response = requests.post(url, json=appointment_data, timeout=10)
            
            if response.status_code == 201:
                self.log_pass("預約建立", "API成功建立預約")
                # 檢查回應格式
                data = response.json()
                expected_fields = ['id', 'user', 'therapist', 'status', 'detail']
                missing_fields = [field for field in expected_fields if field not in data]
                
                if missing_fields:
                    self.log_warning("預約回應格式", f"缺少欄位: {missing_fields}")
                else:
                    self.log_pass("預約回應格式", "回應格式正確")
                    
            else:
                self.log_error("預約建立", f"API回應碼: {response.status_code}, 內容: {response.text}")
                
        except Exception as e:
            self.log_error("預約建立", f"測試失敗: {e}")

    def test_data_consistency(self):
        """測試資料一致性"""
        print("\n🔍 測試資料一致性...")
        
        # 檢查是否有專業領域資料
        try:
            specialty_count = Specialty.objects.count()
            if specialty_count > 0:
                self.log_pass("專業領域資料", f"共有 {specialty_count} 個專業領域")
            else:
                self.log_warning("專業領域資料", "沒有專業領域資料，請執行初始化指令")
        except Exception as e:
            self.log_error("專業領域資料", f"檢查失敗: {e}")

        # 檢查是否有心理師資料
        try:
            therapist_count = TherapistProfile.objects.count()
            if therapist_count > 0:
                self.log_pass("心理師資料", f"共有 {therapist_count} 位心理師")
                
                # 檢查心理師是否都有專業領域
                therapists_without_specialties = TherapistProfile.objects.filter(specialties=None).count()
                if therapists_without_specialties > 0:
                    self.log_warning("心理師專業領域", f"{therapists_without_specialties} 位心理師沒有專業領域")
            else:
                self.log_warning("心理師資料", "沒有心理師資料")
        except Exception as e:
            self.log_error("心理師資料", f"檢查失敗: {e}")

        # 檢查測驗系統
        try:
            test_count = Test.objects.count()
            if test_count > 0:
                self.log_pass("心理測驗", f"共有 {test_count} 個測驗")
                
                # 檢查測驗是否有題目
                for test in Test.objects.all():
                    question_count = Question.objects.filter(test=test).count()
                    if question_count == 0:
                        self.log_warning(f"測驗 {test.name}", "沒有題目")
            else:
                self.log_warning("心理測驗", "沒有測驗資料")
        except Exception as e:
            self.log_error("心理測驗", f"檢查失敗: {e}")

    def test_frontend_backend_compatibility(self):
        """測試前後端相容性"""
        print("\n🔗 測試前後端相容性...")
        
        # 測試前端是否能訪問後端API
        try:
            # 模擬前端CORS請求
            headers = {
                'Origin': self.frontend_url,
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = requests.options(f"{self.backend_url}/api/therapists/profiles/", 
                                      headers=headers, timeout=5)
            
            if 'Access-Control-Allow-Origin' in response.headers:
                self.log_pass("CORS設定", "後端允許前端跨域請求")
            else:
                self.log_warning("CORS設定", "可能存在CORS問題")
                
        except Exception as e:
            self.log_error("CORS測試", f"測試失敗: {e}")

        # 檢查前端API介面定義
        try:
            # 這裡可以檢查TypeScript介面定義是否與後端一致
            # 由於無法直接讀取TypeScript，我們檢查API回應格式
            
            response = requests.get(f"{self.backend_url}/api/therapists/profiles/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    therapist = data[0]
                    # 檢查是否有前端期望的欄位
                    expected_fields = ['id', 'name', 'title', 'specialties', 'consultation_modes']
                    missing_fields = [field for field in expected_fields if field not in therapist]
                    
                    if missing_fields:
                        self.log_error("API格式相容性", f"心理師API缺少欄位: {missing_fields}")
                    else:
                        self.log_pass("API格式相容性", "心理師API格式正確")
                        
                    # 檢查是否錯誤包含pricing欄位
                    if 'pricing' in therapist:
                        self.log_warning("API格式相容性", "心理師API仍包含pricing欄位，前端已移除")
                        
        except Exception as e:
            self.log_error("API格式檢查", f"檢查失敗: {e}")

    def test_email_system(self):
        """測試郵件系統設定"""
        print("\n📧 測試郵件系統...")
        
        try:
            from django.conf import settings
            from django.core.mail import send_mail
            
            # 檢查郵件設定
            if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                self.log_pass("郵件設定", f"SMTP主機: {settings.EMAIL_HOST}")
            else:
                self.log_error("郵件設定", "缺少EMAIL_HOST設定")
                
            if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                self.log_pass("郵件認證", "已設定EMAIL_HOST_USER")
            else:
                self.log_warning("郵件認證", "缺少EMAIL_HOST_USER設定")
                
            # 測試郵件通知函數
            try:
                from appointments.notifications import send_appointment_created_notification
                self.log_pass("郵件通知函數", "預約通知函數存在")
            except ImportError:
                self.log_error("郵件通知函數", "無法導入預約通知函數")
                
        except Exception as e:
            self.log_error("郵件系統", f"檢查失敗: {e}")

    def generate_summary(self):
        """生成測試摘要"""
        print("\n" + "="*80)
        print("🎯 測試結果摘要")
        print("="*80)
        
        print(f"✅ 通過: {len(self.passed)}")
        print(f"⚠️  警告: {len(self.warnings)}")  
        print(f"❌ 錯誤: {len(self.errors)}")
        
        if self.errors:
            print("\n❌ 需要修復的錯誤:")
            for error in self.errors:
                print(f"  {error}")
                
        if self.warnings:
            print("\n⚠️  需要注意的警告:")
            for warning in self.warnings:
                print(f"  {warning}")
                
        # 生成修復腳本建議
        if self.errors or self.warnings:
            print("\n🔧 建議的修復步驟:")
            print("1. 執行資料庫遷移: python manage.py migrate")
            print("2. 初始化專業領域: python manage.py init_specialties") 
            print("3. 初始化測驗資料: python manage.py init_who5 && python manage.py init_bsrs5_updated")
            print("4. 檢查.env檔案的郵件設定")
            print("5. 重啟Django和Next.js服務器")

    def run_all_tests(self):
        """執行所有測試"""
        print("🚀 開始綜合系統測試...")
        print(f"📍 後端URL: {self.backend_url}")
        print(f"📍 前端URL: {self.frontend_url}")
        
        self.test_database_models()
        self.test_api_endpoints()
        self.test_appointment_creation()
        self.test_data_consistency()
        self.test_frontend_backend_compatibility()
        self.test_email_system()
        
        self.generate_summary()

if __name__ == "__main__":
    tester = SystemTester()
    tester.run_all_tests()