#!/usr/bin/env python
"""
简化前后端同步检查
"""

import re
import os
from pathlib import Path

class SimpleSyncTester:
    def __init__(self):
        self.issues = []
        self.backend_dir = Path(".")
        self.frontend_dir = Path("../fornt")
        
    def log_issue(self, category, message):
        self.issues.append(f"[{category}] {message}")
        print(f"[ISSUE] {category}: {message}")
        
    def log_pass(self, category, message):
        print(f"[PASS] {category}: {message}")

    def check_frontend_files_exist(self):
        print("\n=== Checking Frontend Files ===")
        
        # Check if frontend directory exists
        if not self.frontend_dir.exists():
            self.log_issue("Frontend", f"Frontend directory not found: {self.frontend_dir}")
            return False
            
        # Check key files
        key_files = [
            "lib/api.ts",
            "app/appointments/book/page.tsx",
            "app/appointments/query/page.tsx"
        ]
        
        for file_path in key_files:
            full_path = self.frontend_dir / file_path
            if full_path.exists():
                self.log_pass("Frontend Files", f"{file_path} exists")
            else:
                self.log_issue("Frontend Files", f"Missing: {file_path}")
                
        return True

    def check_api_interface(self):
        print("\n=== Checking API Interface ===")
        
        api_file = self.frontend_dir / "lib" / "api.ts"
        
        if not api_file.exists():
            self.log_issue("API Interface", "api.ts not found")
            return
            
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check API_BASE_URL configuration
            if "API_BASE_URL = ''" in content:
                self.log_issue("API Config", "API_BASE_URL is empty string")
            elif "localhost:8000" in content:
                self.log_pass("API Config", "API_BASE_URL points to Django")
            else:
                self.log_issue("API Config", "API_BASE_URL configuration unclear")
                
            # Check for pricing field (should not exist)
            if 'pricing:' in content:
                self.log_issue("API Interface", "Still contains pricing field definition")
            else:
                self.log_pass("API Interface", "No pricing field (correct)")
                
            # Check key API functions exist
            api_functions = [
                'getTherapists', 'getSpecialties', 'createAppointment', 
                'queryAppointments'
            ]
            
            missing_functions = []
            for func in api_functions:
                if f"export async function {func}" not in content:
                    missing_functions.append(func)
                    
            if missing_functions:
                self.log_issue("API Functions", f"Missing: {missing_functions}")
            else:
                self.log_pass("API Functions", "All key functions present")
                
        except Exception as e:
            self.log_issue("API Interface", f"Failed to read api.ts: {e}")

    def check_booking_page(self):
        print("\n=== Checking Booking Page ===")
        
        book_page = self.frontend_dir / "app" / "appointments" / "book" / "page.tsx"
        
        if not book_page.exists():
            self.log_issue("Booking Page", "page.tsx not found")
            return
            
        try:
            with open(book_page, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for pricing references (should not exist)
            pricing_references = []
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                if 'pricing' in line.lower() and not line.strip().startswith('//'):
                    pricing_references.append(f"Line {i}: {line.strip()}")
                    
            if pricing_references:
                self.log_issue("Booking Page", f"Found pricing references: {len(pricing_references)}")
                for ref in pricing_references[:3]:  # Show first 3
                    print(f"  {ref}")
            else:
                self.log_pass("Booking Page", "No pricing references found")
                
            # Check API imports
            required_imports = ['getSpecialties', 'getTherapists', 'createAppointment']
            missing_imports = []
            
            for import_name in required_imports:
                if import_name not in content:
                    missing_imports.append(import_name)
                    
            if missing_imports:
                self.log_issue("Booking Page", f"Missing imports: {missing_imports}")
            else:
                self.log_pass("Booking Page", "All required imports present")
                
        except Exception as e:
            self.log_issue("Booking Page", f"Failed to read booking page: {e}")

    def check_typescript_interfaces(self):
        print("\n=== Checking TypeScript Interfaces ===")
        
        api_file = self.frontend_dir / "lib" / "api.ts"
        
        if not api_file.exists():
            return
            
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check TherapistProfile interface
            if 'export interface TherapistProfile' in content:
                self.log_pass("TS Interfaces", "TherapistProfile interface exists")
                
                # Extract the interface content
                match = re.search(r'export interface TherapistProfile\s*{([^}]+)}', 
                                content, re.DOTALL)
                
                if match:
                    interface_content = match.group(1)
                    
                    # Check for pricing field
                    if 'pricing:' in interface_content:
                        self.log_issue("TherapistProfile", "Still contains pricing field")
                    else:
                        self.log_pass("TherapistProfile", "No pricing field (correct)")
                        
                    # Check for required fields
                    required_fields = [
                        'id:', 'name:', 'title:', 'specialties:', 
                        'consultation_modes:'
                    ]
                    
                    missing_fields = [f.replace(':', '') for f in required_fields 
                                    if f not in interface_content]
                    
                    if missing_fields:
                        self.log_issue("TherapistProfile", f"Missing fields: {missing_fields}")
                    else:
                        self.log_pass("TherapistProfile", "All required fields present")
            else:
                self.log_issue("TS Interfaces", "TherapistProfile interface not found")
                
            # Check AppointmentResponse interface
            if 'export interface AppointmentResponse' in content:
                self.log_pass("TS Interfaces", "AppointmentResponse interface exists")
            else:
                self.log_issue("TS Interfaces", "AppointmentResponse interface missing")
                
        except Exception as e:
            self.log_issue("TS Interfaces", f"Failed to parse interfaces: {e}")

    def generate_summary(self):
        print("\n" + "="*60)
        print("FRONTEND-BACKEND SYNC TEST SUMMARY")
        print("="*60)
        
        if not self.issues:
            print("SUCCESS: Frontend and backend are in sync!")
            return
            
        print(f"SYNC ISSUES FOUND: {len(self.issues)}")
        print("\nDETAILS:")
        for issue in self.issues:
            print(f"  {issue}")
            
        print("\nRECOMMENDATIONS:")
        
        has_pricing = any('pricing' in issue.lower() for issue in self.issues)
        if has_pricing:
            print("- Remove all pricing-related code from frontend")
            
        has_api_config = any('api config' in issue.lower() for issue in self.issues)
        if has_api_config:
            print("- Fix API_BASE_URL configuration in lib/api.ts")
            
        has_missing_files = any('missing' in issue.lower() for issue in self.issues)
        if has_missing_files:
            print("- Ensure all required frontend files exist")

    def run_sync_check(self):
        print("FRONTEND-BACKEND SYNC CHECK")
        print("Backend Dir:", self.backend_dir.absolute())
        print("Frontend Dir:", self.frontend_dir.absolute())
        print("="*60)
        
        if not self.check_frontend_files_exist():
            print("Cannot proceed without frontend files")
            return
            
        self.check_api_interface()
        self.check_typescript_interfaces()
        self.check_booking_page()
        
        self.generate_summary()

if __name__ == "__main__":
    tester = SimpleSyncTester()
    tester.run_sync_check()