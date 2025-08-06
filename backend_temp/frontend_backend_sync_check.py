#!/usr/bin/env python
"""
前後端同步檢查腳本
檢查前端TypeScript介面與後端Django模型的一致性
"""

import re
import os
import json
from pathlib import Path

class FrontendBackendSyncChecker:
    def __init__(self):
        self.issues = []
        self.backend_dir = Path(".")
        self.frontend_dir = Path("../fornt")
        
    def log_issue(self, category: str, severity: str, message: str):
        self.issues.append({
            'category': category,
            'severity': severity, 
            'message': message
        })
        
        icon = "🔴" if severity == "ERROR" else "🟡" if severity == "WARNING" else "🔵"
        print(f"{icon} [{category}] {message}")

    def parse_typescript_interfaces(self):
        """解析前端TypeScript介面定義"""
        api_file = self.frontend_dir / "lib" / "api.ts"
        
        if not api_file.exists():
            self.log_issue("Frontend", "ERROR", f"找不到 {api_file}")
            return {}
            
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 解析介面定義
            interfaces = {}
            
            # 匹配 export interface 定義
            interface_pattern = r'export interface (\w+)\s*{([^}]+)}'
            matches = re.finditer(interface_pattern, content, re.DOTALL)
            
            for match in matches:
                interface_name = match.group(1)
                interface_body = match.group(2)
                
                # 解析欄位
                fields = {}
                field_pattern = r'(\w+)(\?)?:\s*([^;]+);'
                field_matches = re.finditer(field_pattern, interface_body)
                
                for field_match in field_matches:
                    field_name = field_match.group(1)
                    is_optional = field_match.group(2) == '?'
                    field_type = field_match.group(3).strip()
                    
                    fields[field_name] = {
                        'type': field_type,
                        'optional': is_optional
                    }
                    
                interfaces[interface_name] = fields
                
            return interfaces
            
        except Exception as e:
            self.log_issue("Frontend", "ERROR", f"解析 api.ts 失敗: {e}")
            return {}

    def get_django_model_fields(self):
        """獲取Django模型欄位定義"""
        models = {}
        
        # 讀取各app的models.py
        apps = ['therapists', 'appointments', 'articles', 'assessments', 'users']
        
        for app in apps:
            models_file = self.backend_dir / app / "models.py"
            if models_file.exists():
                try:
                    with open(models_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # 簡單的模型解析（不執行Python代碼）
                    class_pattern = r'class (\w+)\([^)]*models\.Model[^)]*\):'
                    matches = re.finditer(class_pattern, content)
                    
                    for match in matches:
                        model_name = match.group(1)
                        if model_name not in models:
                            models[model_name] = {'app': app, 'fields': []}
                            
                except Exception as e:
                    self.log_issue("Backend", "WARNING", f"讀取 {models_file} 失敗: {e}")
                    
        return models

    def check_therapist_interface(self):
        """檢查TherapistProfile介面"""
        print("\n👨‍⚕️ 檢查TherapistProfile介面...")
        
        interfaces = self.parse_typescript_interfaces()
        therapist_interface = interfaces.get('TherapistProfile', {})
        
        if not therapist_interface:
            self.log_issue("TherapistProfile", "ERROR", "前端缺少TherapistProfile介面")
            return
            
        # 預期欄位（基於實際後端serializer）
        expected_fields = {
            'id': 'number',
            'name': 'string', 
            'title': 'string',
            'license_number': 'string',
            'education': 'string',
            'experience': 'string',
            'specialties': 'Specialty[]',
            'specialties_display': 'string',
            'specialties_list': 'string[]',
            'beliefs': 'string',
            'photo': 'string | null',
            'available_times': 'AvailableTime[]',
            'consultation_modes': 'string[]',
            'created_at': 'string'
        }
        
        # 檢查缺少的欄位
        for field, expected_type in expected_fields.items():
            if field not in therapist_interface:
                self.log_issue("TherapistProfile", "WARNING", 
                             f"前端介面缺少欄位: {field}: {expected_type}")
            else:
                frontend_type = therapist_interface[field]['type']
                if frontend_type != expected_type:
                    self.log_issue("TherapistProfile", "INFO",
                                 f"類型不匹配 {field}: 前端={frontend_type}, 期望={expected_type}")
                                 
        # 檢查多餘的欄位
        for field in therapist_interface:
            if field not in expected_fields:
                if field == 'pricing':
                    self.log_issue("TherapistProfile", "ERROR",
                                 "前端仍有pricing欄位，但後端已移除此功能")
                else:
                    self.log_issue("TherapistProfile", "INFO",
                                 f"前端有額外欄位: {field}")

    def check_appointment_interface(self):
        """檢查預約相關介面"""
        print("\n📅 檢查預約介面...")
        
        interfaces = self.parse_typescript_interfaces()
        
        # 檢查AppointmentResponse介面
        appointment_response = interfaces.get('AppointmentResponse', {})
        if appointment_response:
            expected_fields = {
                'id': 'number',
                'user': 'string',
                'therapist': 'string', 
                'slot': 'AvailableSlotResponse | null',
                'consultation_type': 'string',
                'consultation_type_display': 'string',
                'price': 'string',
                'status': 'string',
                'status_display': 'string',
                'created_at': 'string',
                'preferred_periods': 'PreferredPeriodResponse[]',
                'detail': 'AppointmentDetail'
            }
            
            for field, expected_type in expected_fields.items():
                if field not in appointment_response:
                    self.log_issue("AppointmentResponse", "WARNING",
                                 f"缺少欄位: {field}: {expected_type}")
        else:
            self.log_issue("AppointmentResponse", "ERROR", "缺少AppointmentResponse介面")
            
        # 檢查AppointmentCreateRequest介面
        create_request = interfaces.get('AppointmentCreateRequest', {})
        if create_request:
            required_fields = ['email', 'id_number', 'consultation_type']
            for field in required_fields:
                if field not in create_request:
                    self.log_issue("AppointmentCreateRequest", "ERROR",
                                 f"缺少必要欄位: {field}")
        else:
            self.log_issue("AppointmentCreateRequest", "ERROR", 
                         "缺少AppointmentCreateRequest介面")

    def check_api_endpoints(self):
        """檢查API端點定義"""
        print("\n🌐 檢查API端點...")
        
        api_file = self.frontend_dir / "lib" / "api.ts"
        
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 檢查API_BASE_URL設定
            if "API_BASE_URL = ''" in content:
                self.log_issue("API Config", "ERROR", 
                             "API_BASE_URL設為空字串，可能導致連接問題")
            elif "localhost:8000" in content:
                self.log_issue("API Config", "INFO",
                             "API_BASE_URL設為localhost:8000（開發模式）")
                             
            # 檢查關鍵API函數
            api_functions = [
                'getTherapists', 'getSpecialties', 'createAppointment', 
                'queryAppointments', 'getArticles', 'getAssessmentTests'
            ]
            
            for func in api_functions:
                if f"export async function {func}" not in content:
                    self.log_issue("API Functions", "WARNING",
                                 f"缺少API函數: {func}")
                                 
        except Exception as e:
            self.log_issue("API Endpoints", "ERROR", f"檢查失敗: {e}")

    def check_component_usage(self):
        """檢查前端元件中的API使用"""
        print("\n⚛️  檢查前端元件...")
        
        # 檢查預約頁面
        book_page = self.frontend_dir / "app" / "appointments" / "book" / "page.tsx"
        
        if book_page.exists():
            try:
                with open(book_page, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 檢查是否還有pricing相關代碼
                if 'pricing' in content.lower():
                    self.log_issue("Book Page", "WARNING",
                                 "預約頁面仍包含pricing相關代碼")
                                 
                # 檢查API導入
                required_imports = ['getSpecialties', 'getTherapists', 'createAppointment']
                for import_name in required_imports:
                    if import_name not in content:
                        self.log_issue("Book Page", "WARNING",
                                     f"未導入API函數: {import_name}")
                                     
            except Exception as e:
                self.log_issue("Book Page", "ERROR", f"檢查失敗: {e}")
        else:
            self.log_issue("Book Page", "ERROR", "找不到預約頁面")

    def generate_sync_report(self):
        """生成同步報告"""
        print("\n" + "="*80)
        print("🔗 前後端同步檢查報告")  
        print("="*80)
        
        if not self.issues:
            print("🎉 前後端完全同步！")
            return
            
        # 按類別分組
        categories = {}
        for issue in self.issues:
            category = issue['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(issue)
            
        for category, issues in categories.items():
            print(f"\n📋 {category}:")
            for issue in issues:
                severity_icon = {
                    'ERROR': '🔴',
                    'WARNING': '🟡', 
                    'INFO': '🔵'
                }[issue['severity']]
                print(f"  {severity_icon} {issue['message']}")
                
        # 生成修復建議
        print(f"\n🔧 同步修復建議:")
        
        has_pricing_issues = any('pricing' in issue['message'].lower() for issue in self.issues)
        if has_pricing_issues:
            print("• 完全移除前後端所有pricing相關代碼")
            
        has_interface_issues = any(issue['category'].endswith('Profile') or 
                                 issue['category'].endswith('Response') 
                                 for issue in self.issues)
        if has_interface_issues:
            print("• 更新前端TypeScript介面以匹配後端serializer")
            
        has_api_issues = any('API' in issue['category'] for issue in self.issues)
        if has_api_issues:
            print("• 檢查API端點URL和函數定義")
            print("• 確保前端API調用與後端路由一致")

    def run_sync_check(self):
        """執行同步檢查"""
        print("🔗 開始前後端同步檢查...")
        
        # 檢查前端目錄是否存在
        if not self.frontend_dir.exists():
            self.log_issue("Frontend", "ERROR", f"找不到前端目錄: {self.frontend_dir}")
            return
            
        self.check_therapist_interface()
        self.check_appointment_interface()
        self.check_api_endpoints()
        self.check_component_usage()
        
        self.generate_sync_report()

if __name__ == "__main__":
    checker = FrontendBackendSyncChecker()
    checker.run_sync_check()