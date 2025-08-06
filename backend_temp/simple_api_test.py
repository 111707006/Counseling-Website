#!/usr/bin/env python
"""
简化API兼容性测试
"""

import requests
import json

class SimpleAPITester:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000"
        self.issues = []
        
    def log_issue(self, api_name, message):
        self.issues.append(f"[{api_name}] {message}")
        print(f"[ISSUE] {api_name}: {message}")
        
    def log_pass(self, api_name, message):
        print(f"[PASS] {api_name}: {message}")

    def check_therapist_api(self):
        print("\n=== Checking Therapist API ===")
        
        try:
            response = requests.get(f"{self.backend_url}/api/therapists/profiles/")
            if response.status_code != 200:
                self.log_issue("Therapists API", f"HTTP {response.status_code}")
                return
                
            data = response.json()
            if not data:
                self.log_issue("Therapists API", "No data returned")
                return
                
            therapist = data[0]
            
            # Check expected fields
            required_fields = [
                'id', 'name', 'title', 'license_number', 'education',
                'experience', 'specialties', 'specialties_display', 
                'beliefs', 'consultation_modes', 'created_at'
            ]
            
            missing_fields = []
            for field in required_fields:
                if field not in therapist:
                    missing_fields.append(field)
                    
            if missing_fields:
                self.log_issue("Therapists API", f"Missing fields: {missing_fields}")
            else:
                self.log_pass("Therapists API", "All required fields present")
            
            # Check for deprecated fields
            if 'pricing' in therapist:
                self.log_issue("Therapists API", "Still contains deprecated 'pricing' field")
            else:
                self.log_pass("Therapists API", "No deprecated pricing field")
                
            # Check specialties structure
            if 'specialties' in therapist and therapist['specialties']:
                specialty = therapist['specialties'][0]
                specialty_fields = ['id', 'name', 'description', 'is_active']
                specialty_missing = [f for f in specialty_fields if f not in specialty]
                
                if specialty_missing:
                    self.log_issue("Specialties Structure", f"Missing: {specialty_missing}")
                else:
                    self.log_pass("Specialties Structure", "Complete")
                    
        except Exception as e:
            self.log_issue("Therapists API", f"Exception: {e}")

    def check_appointment_api(self):
        print("\n=== Checking Appointment API ===")
        
        # Test appointment creation
        test_data = {
            "email": "api_test_user@example.com",
            "id_number": "B123456789",
            "consultation_type": "online", 
            "name": "API Test User",
            "phone": "0987654321",
            "main_concerns": "Testing API compatibility",
            "urgency": "low"
        }
        
        try:
            response = requests.post(f"{self.backend_url}/api/appointments/", json=test_data)
            
            if response.status_code == 201:
                self.log_pass("Appointment Creation", "Successfully created")
                
                data = response.json()
                
                # Check response structure
                expected_fields = [
                    'id', 'user', 'therapist', 'consultation_type',
                    'consultation_type_display', 'status', 'status_display',
                    'created_at', 'detail'
                ]
                
                missing_fields = [f for f in expected_fields if f not in data]
                
                if missing_fields:
                    self.log_issue("Appointment Response", f"Missing fields: {missing_fields}")
                else:
                    self.log_pass("Appointment Response", "Structure correct")
                
                # Check detail structure
                if 'detail' in data and isinstance(data['detail'], dict):
                    detail = data['detail']
                    detail_fields = ['name', 'phone', 'main_concerns', 'urgency']
                    detail_missing = [f for f in detail_fields if f not in detail]
                    
                    if detail_missing:
                        self.log_issue("Appointment Detail", f"Missing: {detail_missing}")
                    else:
                        self.log_pass("Appointment Detail", "Structure correct")
                        
            else:
                self.log_issue("Appointment Creation", 
                             f"Failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_issue("Appointment API", f"Exception: {e}")

    def check_specialties_api(self):
        print("\n=== Checking Specialties API ===")
        
        try:
            response = requests.get(f"{self.backend_url}/api/therapists/specialties/")
            
            if response.status_code != 200:
                self.log_issue("Specialties API", f"HTTP {response.status_code}")
                return
                
            data = response.json()
            if not data:
                self.log_issue("Specialties API", "No data returned")
                return
                
            specialty = data[0]
            required_fields = ['id', 'name', 'description', 'is_active']
            
            missing_fields = [f for f in required_fields if f not in specialty]
            
            if missing_fields:
                self.log_issue("Specialties API", f"Missing fields: {missing_fields}")
            else:
                self.log_pass("Specialties API", f"Structure correct, {len(data)} specialties")
                
        except Exception as e:
            self.log_issue("Specialties API", f"Exception: {e}")

    def check_articles_api(self):
        print("\n=== Checking Articles API ===")
        
        try:
            response = requests.get(f"{self.backend_url}/api/articles/articles/")
            
            if response.status_code != 200:
                self.log_issue("Articles API", f"HTTP {response.status_code}")
                return
                
            data = response.json()
            self.log_pass("Articles API", f"Accessible, {len(data)} articles")
            
            if data:  # If there are articles
                article = data[0]
                expected_fields = [
                    'id', 'title', 'excerpt', 'content', 'author_name',
                    'published_at', 'is_published'
                ]
                
                missing_fields = [f for f in expected_fields if f not in article]
                
                if missing_fields:
                    self.log_issue("Articles Structure", f"Missing: {missing_fields}")
                else:
                    self.log_pass("Articles Structure", "Complete")
                    
        except Exception as e:
            self.log_issue("Articles API", f"Exception: {e}")

    def check_assessments_api(self):
        print("\n=== Checking Assessments API ===")
        
        try:
            response = requests.get(f"{self.backend_url}/api/assessments/tests/")
            
            if response.status_code != 200:
                self.log_issue("Assessments API", f"HTTP {response.status_code}")
                return
                
            data = response.json()
            self.log_pass("Assessments API", f"Accessible, {len(data)} tests")
            
            if data:
                test = data[0]
                expected_fields = ['code', 'name', 'description']
                
                missing_fields = [f for f in expected_fields if f not in test]
                
                if missing_fields:
                    self.log_issue("Assessment Structure", f"Missing: {missing_fields}")
                else:
                    self.log_pass("Assessment Structure", "Complete")
                    
                # Test questions endpoint
                test_code = test.get('code')
                if test_code:
                    questions_response = requests.get(
                        f"{self.backend_url}/api/assessments/tests/{test_code}/questions/"
                    )
                    
                    if questions_response.status_code == 200:
                        questions = questions_response.json()
                        self.log_pass("Assessment Questions", f"{len(questions)} questions for {test_code}")
                    else:
                        self.log_issue("Assessment Questions", 
                                     f"Failed for {test_code}: {questions_response.status_code}")
                        
        except Exception as e:
            self.log_issue("Assessments API", f"Exception: {e}")

    def generate_summary(self):
        print("\n" + "="*60)
        print("API COMPATIBILITY TEST SUMMARY")
        print("="*60)
        
        if not self.issues:
            print("SUCCESS: All API endpoints are compatible!")
            return
            
        print(f"ISSUES FOUND: {len(self.issues)}")
        print("\nDETAILS:")
        for issue in self.issues:
            print(f"  {issue}")
            
        print("\nRECOMMENDATIONS:")
        
        has_pricing = any('pricing' in issue.lower() for issue in self.issues)
        if has_pricing:
            print("- Remove all pricing-related code from backend serializers")
            
        has_missing_fields = any('missing' in issue.lower() for issue in self.issues)
        if has_missing_fields:
            print("- Update serializers to include all required fields")
            print("- Check model field definitions")
            
        has_structure = any('structure' in issue.lower() for issue in self.issues)
        if has_structure:
            print("- Verify nested object serialization")

    def run_all_checks(self):
        print("API COMPATIBILITY TEST")
        print("Backend URL:", self.backend_url)
        print("="*60)
        
        self.check_therapist_api()
        self.check_specialties_api()
        self.check_appointment_api()
        self.check_articles_api()
        self.check_assessments_api()
        
        self.generate_summary()

if __name__ == "__main__":
    tester = SimpleAPITester()
    tester.run_all_checks()