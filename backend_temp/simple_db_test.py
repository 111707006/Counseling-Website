#!/usr/bin/env python
"""
简化数据库完整性检查
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model
from therapists.models import TherapistProfile, Specialty
from appointments.models import Appointment, PreferredPeriod, AppointmentDetail

User = get_user_model()

class SimpleDBTester:
    def __init__(self):
        self.issues = []
        self.fixes = []
        
    def log_issue(self, category, severity, message, fix=None):
        self.issues.append({
            'category': category,
            'severity': severity,
            'message': message,
            'fix': fix
        })
        
        prefix = "[ERROR]" if severity == "ERROR" else "[WARN]" if severity == "WARNING" else "[INFO]"
        print(f"{prefix} {category}: {message}")
        
        if fix:
            self.fixes.append(fix)
            print(f"  FIX: {fix}")

    def check_migrations(self):
        print("\n=== Checking Migration Status ===")
        
        try:
            from django.db.migrations.executor import MigrationExecutor
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            
            if plan:
                self.log_issue("Migration", "ERROR", 
                             f"{len(plan)} pending migrations",
                             "Run: python manage.py migrate")
                             
                for migration, backwards in plan:
                    print(f"  PENDING: {migration}")
            else:
                print("[PASS] All migrations applied")
                
        except Exception as e:
            self.log_issue("Migration", "ERROR", f"Check failed: {e}")

    def check_user_model(self):
        print("\n=== Checking User Model ===")
        
        # Check required fields
        user_fields = [field.name for field in User._meta.fields]
        required_fields = ['email', 'id_number_hash']
        
        missing_fields = [f for f in required_fields if f not in user_fields]
        
        if missing_fields:
            self.log_issue("User Model", "ERROR", 
                         f"Missing fields: {missing_fields}",
                         "Update users/models.py")
        else:
            print("[PASS] User model has required fields")
            
        # Check methods
        user_instance = User()
        required_methods = ['set_id_number', 'check_id_number']
        
        missing_methods = [m for m in required_methods if not hasattr(user_instance, m)]
        
        if missing_methods:
            self.log_issue("User Model", "ERROR",
                         f"Missing methods: {missing_methods}",
                         "Add methods to users/models.py")
        else:
            print("[PASS] User model has required methods")

    def check_appointment_model(self):
        print("\n=== Checking Appointment Models ===")
        
        # Check Appointment fields
        appointment_fields = [field.name for field in Appointment._meta.fields]
        required_fields = [
            'user', 'therapist', 'consultation_type', 
            'price', 'status', 'created_at'
        ]
        
        missing_fields = [f for f in required_fields if f not in appointment_fields]
        
        if missing_fields:
            self.log_issue("Appointment", "ERROR",
                         f"Missing fields: {missing_fields}")
        else:
            print("[PASS] Appointment model structure correct")
            
        # Check AppointmentDetail model
        try:
            detail_fields = [field.name for field in AppointmentDetail._meta.fields]
            required_detail_fields = [
                'appointment', 'name', 'phone', 'main_concerns', 
                'previous_therapy', 'urgency'
            ]
            
            missing_detail_fields = [f for f in required_detail_fields if f not in detail_fields]
            
            if missing_detail_fields:
                self.log_issue("AppointmentDetail", "ERROR",
                             f"Missing fields: {missing_detail_fields}")
            else:
                print("[PASS] AppointmentDetail model structure correct")
                
        except Exception as e:
            self.log_issue("AppointmentDetail", "ERROR", f"Check failed: {e}")

    def check_data_consistency(self):
        print("\n=== Checking Data Consistency ===")
        
        try:
            # Check orphaned details
            orphaned_details = AppointmentDetail.objects.filter(appointment=None).count()
            if orphaned_details > 0:
                self.log_issue("Data Consistency", "WARNING",
                             f"{orphaned_details} orphaned AppointmentDetail records",
                             "Clean up orphaned records")
            else:
                print("[PASS] No orphaned AppointmentDetail records")
                
        except Exception as e:
            print(f"[INFO] Cannot check AppointmentDetail consistency: {e}")
            
        try:
            # Check appointments without details
            appointments_without_detail = Appointment.objects.filter(detail=None).count()
            if appointments_without_detail > 0:
                self.log_issue("Data Consistency", "WARNING",
                             f"{appointments_without_detail} appointments without detail",
                             "Create AppointmentDetail for these appointments")
            else:
                print("[PASS] All appointments have detail records")
                
        except Exception as e:
            print(f"[INFO] Cannot check appointment details: {e}")
            
        try:
            # Check therapists without specialties
            therapists_without_specialties = TherapistProfile.objects.filter(
                specialties=None
            ).count()
            
            if therapists_without_specialties > 0:
                self.log_issue("Data Consistency", "INFO",
                             f"{therapists_without_specialties} therapists without specialties",
                             "Add specialties via admin interface")
            else:
                print("[PASS] All therapists have specialties")
                
        except Exception as e:
            print(f"[INFO] Cannot check therapist specialties: {e}")

    def check_foreign_keys(self):
        print("\n=== Checking Foreign Key Relationships ===")
        
        try:
            # Check Appointment foreign keys
            user_field = Appointment._meta.get_field('user')
            if user_field.related_model == User:
                print("[PASS] Appointment.user FK correct")
            else:
                self.log_issue("FK Constraint", "ERROR", "Appointment.user FK incorrect")
                
            therapist_field = Appointment._meta.get_field('therapist')
            if therapist_field.related_model == TherapistProfile:
                print("[PASS] Appointment.therapist FK correct")
            else:
                self.log_issue("FK Constraint", "ERROR", "Appointment.therapist FK incorrect")
                
        except Exception as e:
            self.log_issue("FK Constraint", "ERROR", f"FK check failed: {e}")

    def generate_summary(self):
        print("\n" + "="*60)
        print("DATABASE INTEGRITY TEST SUMMARY")
        print("="*60)
        
        if not self.issues:
            print("SUCCESS: Database structure is healthy!")
            return
            
        errors = [i for i in self.issues if i['severity'] == 'ERROR']
        warnings = [i for i in self.issues if i['severity'] == 'WARNING'] 
        infos = [i for i in self.issues if i['severity'] == 'INFO']
        
        print(f"ERRORS: {len(errors)}")
        print(f"WARNINGS: {len(warnings)}")
        print(f"INFO: {len(infos)}")
        
        if errors:
            print("\nCRITICAL ERRORS:")
            for issue in errors:
                print(f"  {issue['category']}: {issue['message']}")
                
        if warnings:
            print("\nWARNINGS:")
            for issue in warnings:
                print(f"  {issue['category']}: {issue['message']}")
                
        if self.fixes:
            print("\nRECOMMENDED FIXES:")
            for fix in self.fixes:
                print(f"  - {fix}")

    def run_all_checks(self):
        print("DATABASE INTEGRITY TEST")
        print("="*60)
        
        self.check_migrations()
        self.check_user_model()
        self.check_appointment_model()
        self.check_data_consistency()
        self.check_foreign_keys()
        
        self.generate_summary()

if __name__ == "__main__":
    tester = SimpleDBTester()
    tester.run_all_checks()