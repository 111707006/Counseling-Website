#!/usr/bin/env python
"""
資料庫完整性檢查腳本
檢查資料庫結構和資料一致性
"""

import os
import sys
import django
from django.db import connection
from django.core.exceptions import ValidationError

# 設置Django環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.contrib.auth import get_user_model
from therapists.models import TherapistProfile, Specialty, AvailableSlot, AvailableTime
from appointments.models import Appointment, PreferredPeriod, AppointmentDetail
from articles.models import Article, ArticleImage
from assessments.models import Test, Question, Choice, Response

User = get_user_model()

class DatabaseIntegrityChecker:
    def __init__(self):
        self.issues = []
        self.fixes = []
        
    def log_issue(self, category: str, severity: str, message: str, fix: str = None):
        self.issues.append({
            'category': category,
            'severity': severity,
            'message': message,
            'fix': fix
        })
        
        icon = "🔴" if severity == "ERROR" else "🟡" if severity == "WARNING" else "🔵"
        print(f"{icon} [{category}] {message}")
        
        if fix:
            self.fixes.append(fix)
            print(f"   💡 修復建議: {fix}")

    def check_migrations(self):
        """檢查資料庫遷移狀態"""
        print("\n📊 檢查資料庫遷移狀態...")
        
        try:
            from django.db.migrations.executor import MigrationExecutor
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            
            if plan:
                self.log_issue("Migration", "ERROR", 
                             f"有 {len(plan)} 個未執行的遷移", 
                             "執行: python manage.py migrate")
                             
                for migration, backwards in plan:
                    print(f"   📋 待執行: {migration}")
            else:
                print("✅ 所有遷移都已執行")
                
        except Exception as e:
            self.log_issue("Migration", "ERROR", f"檢查遷移失敗: {e}")

    def check_user_model(self):
        """檢查User模型"""
        print("\n👤 檢查User模型...")
        
        # 檢查必要欄位
        user_fields = [field.name for field in User._meta.fields]
        required_fields = ['email', 'id_number_hash']
        
        for field in required_fields:
            if field not in user_fields:
                self.log_issue("User Model", "ERROR", 
                             f"缺少必要欄位: {field}",
                             "檢查users/models.py中的User模型定義")
                             
        # 檢查方法
        user_instance = User()
        required_methods = ['set_id_number', 'check_id_number']
        
        for method in required_methods:
            if not hasattr(user_instance, method):
                self.log_issue("User Model", "ERROR",
                             f"缺少必要方法: {method}",
                             "檢查users/models.py中的方法定義")
                             
        # 測試email唯一性約束
        try:
            from django.db import IntegrityError
            # 這只是結構檢查，不實際建立資料
            email_field = User._meta.get_field('email')
            if not email_field.unique:
                self.log_issue("User Model", "WARNING",
                             "email欄位應該設為unique=True")
        except Exception as e:
            self.log_issue("User Model", "WARNING", f"檢查email唯一性失敗: {e}")
            
        print("✅ User模型檢查完成")

    def check_therapist_model(self):
        """檢查TherapistProfile模型"""
        print("\n👨‍⚕️ 檢查TherapistProfile模型...")
        
        # 檢查必要欄位
        therapist_fields = [field.name for field in TherapistProfile._meta.fields]
        required_fields = [
            'name', 'title', 'license_number', 'education', 
            'experience', 'beliefs', 'consultation_modes'
        ]
        
        for field in required_fields:
            if field not in therapist_fields:
                self.log_issue("TherapistProfile", "ERROR",
                             f"缺少必要欄位: {field}",
                             "檢查therapists/models.py中的欄位定義")
                             
        # 檢查關聯欄位
        try:
            specialties_field = TherapistProfile._meta.get_field('specialties')
            if specialties_field.related_model != Specialty:
                self.log_issue("TherapistProfile", "ERROR",
                             "specialties關聯設定錯誤")
        except Exception as e:
            self.log_issue("TherapistProfile", "ERROR", 
                         f"specialties欄位檢查失敗: {e}")
                         
        # 檢查是否誤包含pricing欄位
        if 'pricing' in therapist_fields:
            self.log_issue("TherapistProfile", "WARNING",
                         "仍包含pricing欄位，前端已不使用",
                         "考慮移除pricing欄位或遷移至其他表")
                         
        print("✅ TherapistProfile模型檢查完成")

    def check_appointment_model(self):
        """檢查Appointment相關模型"""
        print("\n📅 檢查Appointment模型...")
        
        # 檢查Appointment欄位
        appointment_fields = [field.name for field in Appointment._meta.fields]
        required_fields = [
            'user', 'therapist', 'slot', 'consultation_type', 
            'price', 'status', 'created_at'
        ]
        
        for field in required_fields:
            if field not in appointment_fields:
                self.log_issue("Appointment", "ERROR",
                             f"缺少必要欄位: {field}")
                             
        # 檢查外鍵關聯
        try:
            user_field = Appointment._meta.get_field('user')
            if user_field.related_model != User:
                self.log_issue("Appointment", "ERROR", "user外鍵設定錯誤")
                
            therapist_field = Appointment._meta.get_field('therapist')  
            if therapist_field.related_model != TherapistProfile:
                self.log_issue("Appointment", "ERROR", "therapist外鍵設定錯誤")
                
        except Exception as e:
            self.log_issue("Appointment", "ERROR", f"外鍵檢查失敗: {e}")
            
        # 檢查AppointmentDetail模型
        detail_fields = [field.name for field in AppointmentDetail._meta.fields]
        required_detail_fields = [
            'appointment', 'name', 'phone', 'main_concerns', 
            'previous_therapy', 'urgency'
        ]
        
        for field in required_detail_fields:
            if field not in detail_fields:
                self.log_issue("AppointmentDetail", "ERROR",
                             f"缺少必要欄位: {field}")
                             
        # 檢查PreferredPeriod模型
        period_fields = [field.name for field in PreferredPeriod._meta.fields]
        if 'appointment' not in period_fields:
            self.log_issue("PreferredPeriod", "ERROR",
                         "缺少appointment外鍵欄位")
                         
        print("✅ Appointment模型檢查完成")

    def check_data_consistency(self):
        """檢查資料一致性"""
        print("\n🔍 檢查資料一致性...")
        
        # 檢查孤立的AppointmentDetail
        try:
            orphaned_details = AppointmentDetail.objects.filter(appointment=None).count()
            if orphaned_details > 0:
                self.log_issue("Data Consistency", "WARNING",
                             f"發現 {orphaned_details} 個孤立的AppointmentDetail記錄",
                             "清理孤立記錄或修復關聯")
        except Exception as e:
            self.log_issue("Data Consistency", "INFO", f"無法檢查AppointmentDetail: {e}")
            
        # 檢查沒有detail的預約
        try:
            appointments_without_detail = Appointment.objects.filter(detail=None).count()
            if appointments_without_detail > 0:
                self.log_issue("Data Consistency", "WARNING",
                             f"發現 {appointments_without_detail} 個沒有detail的預約",
                             "為這些預約建立對應的AppointmentDetail")
        except Exception as e:
            self.log_issue("Data Consistency", "INFO", f"無法檢查Appointment detail: {e}")
            
        # 檢查心理師是否有專業領域
        try:
            therapists_without_specialties = TherapistProfile.objects.filter(
                specialties=None
            ).count()
            if therapists_without_specialties > 0:
                self.log_issue("Data Consistency", "INFO",
                             f"{therapists_without_specialties} 位心理師沒有設定專業領域",
                             "透過admin介面為心理師添加專業領域")
        except Exception as e:
            self.log_issue("Data Consistency", "INFO", f"無法檢查心理師專業領域: {e}")
            
        # 檢查重複的專業領域
        try:
            from django.db.models import Count
            duplicate_specialties = Specialty.objects.values('name').annotate(
                count=Count('name')
            ).filter(count__gt=1)
            
            if duplicate_specialties:
                for dup in duplicate_specialties:
                    self.log_issue("Data Consistency", "WARNING",
                                 f"專業領域名稱重複: {dup['name']} ({dup['count']}次)",
                                 "合併或重新命名重複的專業領域")
        except Exception as e:
            self.log_issue("Data Consistency", "INFO", f"無法檢查專業領域重複: {e}")
            
        print("✅ 資料一致性檢查完成")

    def check_constraints(self):
        """檢查資料庫約束"""
        print("\n🔐 檢查資料庫約束...")
        
        with connection.cursor() as cursor:
            try:
                # 檢查外鍵約束
                cursor.execute("""
                    SELECT TABLE_NAME, CONSTRAINT_NAME 
                    FROM information_schema.TABLE_CONSTRAINTS 
                    WHERE CONSTRAINT_TYPE = 'FOREIGN KEY'
                    AND TABLE_SCHEMA = DATABASE()
                """)
                
                foreign_keys = cursor.fetchall()
                print(f"✅ 發現 {len(foreign_keys)} 個外鍵約束")
                
            except Exception as e:
                # SQLite或其他資料庫可能不支援information_schema
                self.log_issue("Constraints", "INFO", 
                             f"無法檢查約束 (可能使用SQLite): {e}")
                             
        print("✅ 約束檢查完成")

    def generate_fix_script(self):
        """生成修復腳本"""
        if not self.fixes:
            return
            
        print("\n🔧 生成修復腳本...")
        
        script_content = """#!/bin/bash
# 自動生成的資料庫修復腳本
# 執行前請先備份資料庫！

echo "🔧 開始修復資料庫問題..."

"""
        
        # 添加常見修復指令
        script_content += """
# 執行資料庫遷移
echo "📊 執行資料庫遷移..."
python manage.py migrate

# 初始化專業領域資料
echo "🎯 初始化專業領域..."
python manage.py init_specialties

# 初始化測驗資料  
echo "🧠 初始化測驗資料..."
python manage.py init_who5
python manage.py init_bsrs5_updated

"""
        
        # 添加特定修復指令
        for fix in self.fixes:
            if "python manage.py" in fix:
                script_content += f"echo \"🔧 {fix}...\"\n{fix}\n\n"
                
        script_content += """
echo "✅ 修復腳本執行完成"
echo "⚠️  請重啟Django服務器以確保所有變更生效"
"""
        
        with open("database_fix_script.sh", "w", encoding="utf-8") as f:
            f.write(script_content)
            
        print("✅ 修復腳本已生成: database_fix_script.sh")

    def generate_report(self):
        """生成檢查報告"""
        print("\n" + "="*80)
        print("📋 資料庫完整性檢查報告")
        print("="*80)
        
        if not self.issues:
            print("🎉 恭喜！資料庫結構完全正常")
            return
            
        # 按嚴重程度分類
        errors = [i for i in self.issues if i['severity'] == 'ERROR']
        warnings = [i for i in self.issues if i['severity'] == 'WARNING'] 
        infos = [i for i in self.issues if i['severity'] == 'INFO']
        
        print(f"🔴 錯誤: {len(errors)}")
        print(f"🟡 警告: {len(warnings)}")
        print(f"🔵 資訊: {len(infos)}")
        
        if errors:
            print("\n🔴 嚴重錯誤 (需要立即修復):")
            for issue in errors:
                print(f"  [{issue['category']}] {issue['message']}")
                
        if warnings:
            print("\n🟡 警告 (建議修復):")
            for issue in warnings:
                print(f"  [{issue['category']}] {issue['message']}")
                
        if infos:
            print("\n🔵 資訊 (供參考):")
            for issue in infos:
                print(f"  [{issue['category']}] {issue['message']}")

    def run_all_checks(self):
        """執行所有檢查"""
        print("🔍 開始資料庫完整性檢查...")
        
        self.check_migrations()
        self.check_user_model()
        self.check_therapist_model() 
        self.check_appointment_model()
        self.check_data_consistency()
        self.check_constraints()
        
        self.generate_report()
        self.generate_fix_script()

if __name__ == "__main__":
    checker = DatabaseIntegrityChecker()
    checker.run_all_checks()