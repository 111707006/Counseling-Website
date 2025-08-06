#!/usr/bin/env python
"""
API相容性測試腳本
檢查前後端API介面是否一致
"""

import requests
import json
from typing import Dict, List, Any

class APICompatibilityTester:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000"
        self.issues = []
        
    def log_issue(self, api_name: str, issue_type: str, message: str):
        self.issues.append({
            'api': api_name,
            'type': issue_type,
            'message': message
        })
        print(f"⚠️  {api_name} [{issue_type}]: {message}")
        
    def check_therapist_api(self):
        """檢查心理師API"""
        print("\n👨‍⚕️ 檢查心理師API...")
        
        try:
            response = requests.get(f"{self.backend_url}/api/therapists/profiles/")
            if response.status_code != 200:
                self.log_issue("Therapists API", "HTTP_ERROR", f"狀態碼: {response.status_code}")
                return
                
            data = response.json()
            if not data:
                self.log_issue("Therapists API", "NO_DATA", "沒有心理師資料")
                return
                
            therapist = data[0]
            
            # 檢查前端期望的欄位
            frontend_expected = {
                'id': int,
                'name': str,
                'title': str,
                'license_number': str,
                'education': str,
                'experience': str,
                'specialties': list,
                'specialties_display': str,
                'specialties_list': list,
                'beliefs': str,
                'photo': (str, type(None)),
                'available_times': list,
                'consultation_modes': list,
                'created_at': str
            }
            
            for field, expected_type in frontend_expected.items():
                if field not in therapist:
                    self.log_issue("Therapists API", "MISSING_FIELD", f"缺少欄位: {field}")
                else:
                    actual_value = therapist[field]
                    if expected_type == (str, type(None)):
                        if actual_value is not None and not isinstance(actual_value, str):
                            self.log_issue("Therapists API", "TYPE_MISMATCH", 
                                         f"{field} 類型錯誤: 期望 str|null, 實際 {type(actual_value)}")
                    elif not isinstance(actual_value, expected_type):
                        self.log_issue("Therapists API", "TYPE_MISMATCH", 
                                     f"{field} 類型錯誤: 期望 {expected_type}, 實際 {type(actual_value)}")
            
            # 檢查不應該存在的欄位
            if 'pricing' in therapist:
                self.log_issue("Therapists API", "DEPRECATED_FIELD", "仍包含已廢棄的 pricing 欄位")
                
            # 檢查specialties結構
            if 'specialties' in therapist and therapist['specialties']:
                specialty = therapist['specialties'][0]
                specialty_fields = ['id', 'name', 'description', 'is_active']
                for field in specialty_fields:
                    if field not in specialty:
                        self.log_issue("Therapists API", "SPECIALTY_FIELD", f"專業領域缺少欄位: {field}")
                        
            print("✅ 心理師API檢查完成")
            
        except Exception as e:
            self.log_issue("Therapists API", "EXCEPTION", str(e))

    def check_appointment_api(self):
        """檢查預約API"""
        print("\n📅 檢查預約API...")
        
        try:
            # 測試GET請求（可能需要認證）
            response = requests.get(f"{self.backend_url}/api/appointments/")
            if response.status_code == 401:
                print("✅ 預約列表需要認證（正常）")
            elif response.status_code == 200:
                data = response.json()
                if data:
                    appointment = data[0] if isinstance(data, list) else data
                    
                    # 檢查預約欄位
                    expected_fields = [
                        'id', 'user', 'therapist', 'consultation_type', 
                        'consultation_type_display', 'price', 'status', 
                        'status_display', 'created_at', 'preferred_periods', 'detail'
                    ]
                    
                    for field in expected_fields:
                        if field not in appointment:
                            self.log_issue("Appointments API", "MISSING_FIELD", f"缺少欄位: {field}")
                            
            # 測試建立預約
            test_data = {
                "email": "api_test@example.com",
                "id_number": "B987654321", 
                "consultation_type": "online",
                "name": "API測試",
                "phone": "0987654321",
                "main_concerns": "測試API相容性",
                "urgency": "low"
            }
            
            response = requests.post(f"{self.backend_url}/api/appointments/", json=test_data)
            if response.status_code == 201:
                print("✅ 預約建立API正常")
                data = response.json()
                
                # 檢查回應格式
                if 'detail' in data and isinstance(data['detail'], dict):
                    detail = data['detail']
                    detail_fields = ['name', 'phone', 'main_concerns', 'urgency']
                    for field in detail_fields:
                        if field not in detail:
                            self.log_issue("Appointments API", "RESPONSE_FIELD", f"detail缺少欄位: {field}")
                            
            else:
                self.log_issue("Appointments API", "CREATE_ERROR", 
                             f"建立預約失敗: {response.status_code}, {response.text}")
                
        except Exception as e:
            self.log_issue("Appointments API", "EXCEPTION", str(e))

    def check_specialties_api(self):
        """檢查專業領域API"""
        print("\n🎯 檢查專業領域API...")
        
        try:
            response = requests.get(f"{self.backend_url}/api/therapists/specialties/")
            if response.status_code != 200:
                self.log_issue("Specialties API", "HTTP_ERROR", f"狀態碼: {response.status_code}")
                return
                
            data = response.json()
            if not data:
                self.log_issue("Specialties API", "NO_DATA", "沒有專業領域資料")
                return
                
            specialty = data[0]
            expected_fields = ['id', 'name', 'description', 'is_active']
            
            for field in expected_fields:
                if field not in specialty:
                    self.log_issue("Specialties API", "MISSING_FIELD", f"缺少欄位: {field}")
                    
            print("✅ 專業領域API檢查完成")
            
        except Exception as e:
            self.log_issue("Specialties API", "EXCEPTION", str(e))

    def check_articles_api(self):
        """檢查文章API"""  
        print("\n📰 檢查文章API...")
        
        try:
            response = requests.get(f"{self.backend_url}/api/articles/articles/")
            if response.status_code != 200:
                self.log_issue("Articles API", "HTTP_ERROR", f"狀態碼: {response.status_code}")
                return
                
            data = response.json()
            if data:  # 如果有文章資料
                article = data[0]
                expected_fields = [
                    'id', 'title', 'excerpt', 'content', 'tags', 
                    'author_name', 'published_at', 'is_published',
                    'featured_image_url', 'images'
                ]
                
                for field in expected_fields:
                    if field not in article:
                        self.log_issue("Articles API", "MISSING_FIELD", f"缺少欄位: {field}")
                        
            print("✅ 文章API檢查完成")
            
        except Exception as e:
            self.log_issue("Articles API", "EXCEPTION", str(e))

    def check_assessments_api(self):
        """檢查測驗API"""
        print("\n🧠 檢查測驗API...")
        
        try:
            response = requests.get(f"{self.backend_url}/api/assessments/tests/")
            if response.status_code != 200:
                self.log_issue("Assessments API", "HTTP_ERROR", f"狀態碼: {response.status_code}")
                return
                
            data = response.json()
            if data:
                test = data[0]
                expected_fields = ['code', 'name', 'description']
                
                for field in expected_fields:
                    if field not in test:
                        self.log_issue("Assessments API", "MISSING_FIELD", f"缺少欄位: {field}")
                        
                # 測試題目API
                test_code = test.get('code')
                if test_code:
                    questions_response = requests.get(
                        f"{self.backend_url}/api/assessments/tests/{test_code}/questions/"
                    )
                    if questions_response.status_code == 200:
                        questions = questions_response.json()
                        if questions:
                            question = questions[0]
                            question_fields = ['id', 'order', 'text', 'choices']
                            for field in question_fields:
                                if field not in question:
                                    self.log_issue("Assessments API", "QUESTION_FIELD", 
                                                 f"題目缺少欄位: {field}")
                                    
            print("✅ 測驗API檢查完成")
            
        except Exception as e:
            self.log_issue("Assessments API", "EXCEPTION", str(e))

    def generate_compatibility_report(self):
        """生成相容性報告"""
        print("\n" + "="*80)
        print("📋 API相容性檢查報告")
        print("="*80)
        
        if not self.issues:
            print("🎉 恭喜！沒有發現API相容性問題")
            return
            
        # 按API分類問題
        api_issues = {}
        for issue in self.issues:
            api_name = issue['api']
            if api_name not in api_issues:
                api_issues[api_name] = []
            api_issues[api_name].append(issue)
            
        for api_name, issues in api_issues.items():
            print(f"\n🔍 {api_name}:")
            for issue in issues:
                print(f"  [{issue['type']}] {issue['message']}")
                
        # 生成修復建議
        print("\n🔧 修復建議:")
        
        error_types = [issue['type'] for issue in self.issues]
        
        if 'MISSING_FIELD' in error_types:
            print("• 檢查serializers.py是否包含所有必要欄位")
            
        if 'TYPE_MISMATCH' in error_types:
            print("• 檢查模型欄位類型與前端期望是否一致")
            
        if 'DEPRECATED_FIELD' in error_types:
            print("• 從serializers中移除已廢棄的欄位")
            
        if 'NO_DATA' in error_types:
            print("• 執行資料初始化指令")
            print("  - python manage.py init_specialties")
            print("  - 使用admin介面添加心理師資料")
            
        if 'HTTP_ERROR' in error_types:
            print("• 檢查URL路由設定")
            print("• 檢查權限設定")

    def run_all_checks(self):
        """執行所有檢查"""
        print("🔍 開始API相容性檢查...")
        
        self.check_therapist_api()
        self.check_specialties_api()  
        self.check_appointment_api()
        self.check_articles_api()
        self.check_assessments_api()
        
        self.generate_compatibility_report()

if __name__ == "__main__":
    tester = APICompatibilityTester()
    tester.run_all_checks()