#!/usr/bin/env python
"""
简化系统测试脚本 (避免Unicode问题)
"""

import os
import sys
import django
import requests
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.contrib.auth import get_user_model
from therapists.models import TherapistProfile, Specialty
from appointments.models import Appointment
from assessments.models import Test

User = get_user_model()

class SimpleSystemTester:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []
        
    def log_result(self, test_name, status, message):
        if status == "PASS":
            self.passed.append(f"[PASS] {test_name}: {message}")
            print(f"[PASS] {test_name}: {message}")
        elif status == "WARN":
            self.warnings.append(f"[WARN] {test_name}: {message}")
            print(f"[WARN] {test_name}: {message}")
        else:
            self.errors.append(f"[ERROR] {test_name}: {message}")
            print(f"[ERROR] {test_name}: {message}")

    def test_models(self):
        print("\n=== Testing Database Models ===")
        
        # Test User model
        try:
            user = User(email="test@test.com", username="test")
            user.set_id_number("A123456789")
            if hasattr(user, 'check_id_number'):
                self.log_result("User Model", "PASS", "ID number methods exist")
            else:
                self.log_result("User Model", "ERROR", "Missing ID methods")
        except Exception as e:
            self.log_result("User Model", "ERROR", f"Test failed: {e}")
        
        # Test data counts
        try:
            specialty_count = Specialty.objects.count()
            therapist_count = TherapistProfile.objects.count()
            test_count = Test.objects.count()
            
            self.log_result("Data Count", "PASS", 
                          f"Specialties: {specialty_count}, Therapists: {therapist_count}, Tests: {test_count}")
            
            if specialty_count == 0:
                self.log_result("Specialties", "WARN", "No specialty data found")
            
            if therapist_count == 0:
                self.log_result("Therapists", "WARN", "No therapist data found")
                
        except Exception as e:
            self.log_result("Data Count", "ERROR", f"Failed: {e}")

    def test_api_endpoints(self):
        print("\n=== Testing API Endpoints ===")
        
        base_url = "http://127.0.0.1:8000"
        
        endpoints = [
            "/api/therapists/profiles/",
            "/api/therapists/specialties/", 
            "/api/appointments/",
            "/api/articles/articles/",
            "/api/assessments/tests/"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    self.log_result("API", "PASS", f"{endpoint} - Status 200")
                elif response.status_code == 401:
                    self.log_result("API", "PASS", f"{endpoint} - Auth required (401)")
                else:
                    self.log_result("API", "WARN", f"{endpoint} - Status {response.status_code}")
            except requests.exceptions.ConnectionError:
                self.log_result("API", "ERROR", f"{endpoint} - Connection failed")
            except Exception as e:
                self.log_result("API", "ERROR", f"{endpoint} - {e}")

    def test_appointment_creation(self):
        print("\n=== Testing Appointment Creation ===")
        
        appointment_data = {
            "email": "test_appointment@example.com",
            "id_number": "A123456789",
            "consultation_type": "offline",
            "name": "Test User",
            "phone": "0912345678", 
            "main_concerns": "Test appointment functionality"
        }
        
        try:
            response = requests.post("http://127.0.0.1:8000/api/appointments/", 
                                   json=appointment_data, timeout=10)
            
            if response.status_code == 201:
                self.log_result("Appointment", "PASS", "Creation successful")
                
                data = response.json()
                if 'id' in data and 'detail' in data:
                    self.log_result("Appointment Response", "PASS", "Response format correct")
                else:
                    self.log_result("Appointment Response", "WARN", "Missing response fields")
                    
            else:
                self.log_result("Appointment", "ERROR", 
                              f"Creation failed - Status: {response.status_code}")
                              
        except Exception as e:
            self.log_result("Appointment", "ERROR", f"Test failed: {e}")

    def test_cors_settings(self):
        print("\n=== Testing CORS Settings ===")
        
        try:
            headers = {
                'Origin': 'http://localhost:3003',
                'Access-Control-Request-Method': 'GET'
            }
            
            response = requests.options("http://127.0.0.1:8000/api/therapists/profiles/",
                                      headers=headers, timeout=5)
            
            if 'Access-Control-Allow-Origin' in response.headers:
                self.log_result("CORS", "PASS", "CORS headers present")
            else:
                self.log_result("CORS", "WARN", "CORS may not be configured")
                
        except Exception as e:
            self.log_result("CORS", "ERROR", f"Test failed: {e}")

    def test_email_settings(self):
        print("\n=== Testing Email Settings ===")
        
        try:
            from django.conf import settings
            
            if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                self.log_result("Email Config", "PASS", f"SMTP Host: {settings.EMAIL_HOST}")
            else:
                self.log_result("Email Config", "WARN", "No EMAIL_HOST configured")
                
            if hasattr(settings, 'DEFAULT_FROM_EMAIL') and settings.DEFAULT_FROM_EMAIL:
                self.log_result("Email From", "PASS", "Default from email set")
            else:
                self.log_result("Email From", "WARN", "No default from email")
                
        except Exception as e:
            self.log_result("Email Settings", "ERROR", f"Check failed: {e}")

    def generate_summary(self):
        print("\n" + "="*60)
        print("SYSTEM TEST SUMMARY")
        print("="*60)
        
        print(f"PASSED: {len(self.passed)}")
        print(f"WARNINGS: {len(self.warnings)}")
        print(f"ERRORS: {len(self.errors)}")
        
        if self.errors:
            print("\nERRORS THAT NEED FIXING:")
            for error in self.errors:
                print(f"  {error}")
                
        if self.warnings:
            print("\nWARNINGS TO REVIEW:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        print(f"\nTest completed at: {datetime.now()}")
        
        if self.errors:
            print("\nRECOMMENDED ACTIONS:")
            print("1. Run: python manage.py migrate")
            print("2. Run: python manage.py init_specialties")
            print("3. Check .env file for email settings")
            print("4. Restart Django server")

    def run_all_tests(self):
        print("STARTING COMPREHENSIVE SYSTEM TEST")
        print("Backend URL: http://127.0.0.1:8000")
        print("=" * 60)
        
        self.test_models()
        self.test_api_endpoints()
        self.test_appointment_creation()
        self.test_cors_settings()
        self.test_email_settings()
        
        self.generate_summary()

if __name__ == "__main__":
    tester = SimpleSystemTester()
    tester.run_all_tests()