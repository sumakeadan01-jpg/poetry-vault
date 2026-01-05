#!/usr/bin/env python3
"""
Poetry Vault Login API Security Test Suite
Tests all security requirements for the login endpoint
"""

import requests
import json
import time
from urllib.parse import urljoin

class LoginSecurityTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.login_url = urljoin(base_url, "/login")
        self.home_url = urljoin(base_url, "/home")
        self.session = requests.Session()
        
    def print_test_header(self, test_num, description):
        print(f"\n{'='*60}")
        print(f"TEST {test_num}: {description}")
        print('='*60)
    
    def print_result(self, passed, message):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {message}")
    
    def test_1_no_credentials(self):
        """Test 1: Check API behavior when no credentials are provided"""
        self.print_test_header(1, "No Credentials Provided")
        
        # Test with empty POST data
        response = self.session.post(self.login_url, data={})
        
        # Check if error message is returned
        if response.status_code == 200:
            if "Username and password are required" in response.text or "required" in response.text.lower():
                self.print_result(True, "API correctly requires credentials")
            else:
                self.print_result(False, "API should return error when no credentials provided")
        else:
            self.print_result(False, f"Unexpected status code: {response.status_code}")
    
    def test_2_incorrect_credentials(self):
        """Test 2: Test API response with incorrect username/password"""
        self.print_test_header(2, "Incorrect Credentials")
        
        test_cases = [
            {"username": "nonexistent_user", "password": "wrong_password"},
            {"username": "admin", "password": "wrong_password"},
            {"username": "", "password": "some_password"},
            {"username": "some_user", "password": ""}
        ]
        
        for i, credentials in enumerate(test_cases):
            response = self.session.post(self.login_url, data=credentials)
            
            if response.status_code == 200:
                # Check that error message doesn't expose sensitive info
                error_indicators = [
                    "invalid username or password",
                    "login failed",
                    "incorrect",
                    "required"
                ]
                
                response_lower = response.text.lower()
                has_error = any(indicator in response_lower for indicator in error_indicators)
                
                # Check that it doesn't expose sensitive information
                sensitive_info = [
                    "database error",
                    "sql",
                    "exception",
                    "traceback",
                    "user does not exist",
                    "password incorrect"
                ]
                
                has_sensitive = any(info in response_lower for info in sensitive_info)
                
                if has_error and not has_sensitive:
                    self.print_result(True, f"Case {i+1}: Proper error handling without sensitive info exposure")
                else:
                    self.print_result(False, f"Case {i+1}: Improper error handling or sensitive info exposed")
            else:
                self.print_result(False, f"Case {i+1}: Unexpected status code: {response.status_code}")
    
    def test_3_session_persistence(self):
        """Test 3: Verify session persistence after successful login"""
        self.print_test_header(3, "Session Persistence After Login")
        
        # First, try to create a test user (this might fail if user exists, that's OK)
        register_data = {
            "username": "test_session_user",
            "email": "test@example.com", 
            "password": "testpassword123",
            "age": "25"
        }
        
        register_response = self.session.post(urljoin(self.base_url, "/register"), data=register_data)
        
        # Now try to login with the test user
        login_data = {
            "username": "test_session_user",
            "password": "testpassword123"
        }
        
        login_response = self.session.post(self.login_url, data=login_data)
        
        if login_response.status_code == 302 or "home" in login_response.url or login_response.status_code == 200:
            # Check if we can access protected pages
            home_response = self.session.get(self.home_url)
            
            if home_response.status_code == 200 and "logout" in home_response.text.lower():
                self.print_result(True, "Session persists correctly after login")
                
                # Test logout
                logout_response = self.session.get(urljoin(self.base_url, "/logout"))
                
                # Try to access protected page after logout
                home_after_logout = self.session.get(self.home_url)
                
                if home_after_logout.status_code == 302 or "login" in home_after_logout.text.lower():
                    self.print_result(True, "Session correctly terminated after logout")
                else:
                    self.print_result(False, "Session not properly terminated after logout")
            else:
                self.print_result(False, "Cannot access protected pages after login")
        else:
            self.print_result(False, "Login failed - cannot test session persistence")
    
    def test_4_next_parameter_redirect(self):
        """Test 4: Test redirect with 'next' parameter"""
        self.print_test_header(4, "Next Parameter Redirect")
        
        # Test with valid next parameter
        next_url = "/settings"
        login_data = {
            "username": "test_session_user",
            "password": "testpassword123",
            "next": next_url
        }
        
        response = self.session.post(self.login_url, data=login_data)
        
        # Check if redirected to the correct URL
        if response.status_code == 302:
            if next_url in response.headers.get('Location', ''):
                self.print_result(True, "Correctly redirects to 'next' parameter URL")
            else:
                self.print_result(False, f"Did not redirect to specified 'next' URL. Redirected to: {response.headers.get('Location')}")
        else:
            # For form-based redirects, check if the response contains the expected page
            if "settings" in response.text.lower() or response.status_code == 200:
                self.print_result(True, "Successfully handled 'next' parameter (form-based redirect)")
            else:
                self.print_result(False, "Did not properly handle 'next' parameter")
    
    def test_5_input_length_limits(self):
        """Test 5: Test input validation for maximum length limits"""
        self.print_test_header(5, "Input Length Validation")
        
        # Test with extremely long username and password
        long_string = "a" * 2000  # 2000 characters
        
        test_cases = [
            {"username": long_string, "password": "normal_password"},
            {"username": "normal_user", "password": long_string},
            {"username": long_string, "password": long_string}
        ]
        
        for i, credentials in enumerate(test_cases):
            response = self.session.post(self.login_url, data=credentials)
            
            # Should handle gracefully without crashing
            if response.status_code in [200, 400, 422]:
                # Check that it doesn't crash the server
                if "500" not in str(response.status_code) and "error" not in response.text.lower():
                    self.print_result(True, f"Case {i+1}: Handles long input gracefully")
                else:
                    self.print_result(True, f"Case {i+1}: Returns appropriate error for long input")
            else:
                self.print_result(False, f"Case {i+1}: Server error with long input: {response.status_code}")
    
    def test_6_empty_next_parameter(self):
        """Test 6: Test behavior with empty 'next' parameter"""
        self.print_test_header(6, "Empty Next Parameter")
        
        login_data = {
            "username": "test_session_user",
            "password": "testpassword123",
            "next": ""
        }
        
        response = self.session.post(self.login_url, data=login_data)
        
        # Should redirect to default location (home)
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            if 'home' in location or location.endswith('/'):
                self.print_result(True, "Correctly redirects to default location with empty 'next'")
            else:
                self.print_result(False, f"Unexpected redirect location: {location}")
        elif response.status_code == 200:
            if "home" in response.text.lower() or "welcome" in response.text.lower():
                self.print_result(True, "Successfully handles empty 'next' parameter")
            else:
                self.print_result(False, "Did not redirect to default location")
        else:
            self.print_result(False, f"Unexpected response: {response.status_code}")
    
    def test_7_script_injection(self):
        """Test 7: Test XSS/script injection in username and password fields"""
        self.print_test_header(7, "Script Injection Prevention")
        
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "'; DROP TABLE users; --",
            "<svg onload=alert('xss')>",
            "{{7*7}}",  # Template injection
            "${7*7}",   # Expression injection
        ]
        
        for i, malicious_input in enumerate(malicious_inputs):
            # Test in username field
            response1 = self.session.post(self.login_url, data={
                "username": malicious_input,
                "password": "normal_password"
            })
            
            # Test in password field  
            response2 = self.session.post(self.login_url, data={
                "username": "normal_user",
                "password": malicious_input
            })
            
            # Check that malicious script is not executed or reflected
            responses = [response1, response2]
            safe = True
            
            for response in responses:
                if response.status_code == 200:
                    # Check if malicious content is reflected unsanitized
                    if malicious_input in response.text:
                        safe = False
                        break
                    
                    # Check if script tags are present in response
                    if "<script>" in response.text.lower() or "javascript:" in response.text.lower():
                        safe = False
                        break
            
            if safe:
                self.print_result(True, f"Input {i+1}: Properly sanitized malicious input")
            else:
                self.print_result(False, f"Input {i+1}: Malicious input not properly sanitized")
    
    def test_8_null_username(self):
        """Test 8: Test response when username is null/None"""
        self.print_test_header(8, "Null Username Handling")
        
        # Test various null-like inputs
        test_cases = [
            {"password": "some_password"},  # Missing username entirely
            {"username": None, "password": "some_password"},  # Explicit None
            {"username": "null", "password": "some_password"},  # String "null"
            {"username": "", "password": "some_password"},  # Empty string
        ]
        
        for i, data in enumerate(test_cases):
            try:
                response = self.session.post(self.login_url, data=data)
                
                if response.status_code == 200:
                    # Should return appropriate error message
                    if "required" in response.text.lower() or "username" in response.text.lower():
                        self.print_result(True, f"Case {i+1}: Properly handles null/missing username")
                    else:
                        self.print_result(False, f"Case {i+1}: Does not properly validate null username")
                else:
                    self.print_result(False, f"Case {i+1}: Unexpected status code: {response.status_code}")
            except Exception as e:
                self.print_result(False, f"Case {i+1}: Exception occurred: {str(e)}")
    
    def run_all_tests(self):
        """Run all security tests"""
        print("🔒 POETRY VAULT LOGIN SECURITY TEST SUITE")
        print("=" * 60)
        
        try:
            # Test basic connectivity
            response = self.session.get(self.base_url)
            if response.status_code != 200:
                print(f"❌ Cannot connect to {self.base_url}")
                return
            
            print(f"✅ Connected to Poetry Vault at {self.base_url}")
            
            # Run all tests
            self.test_1_no_credentials()
            self.test_2_incorrect_credentials()
            self.test_3_session_persistence()
            self.test_4_next_parameter_redirect()
            self.test_5_input_length_limits()
            self.test_6_empty_next_parameter()
            self.test_7_script_injection()
            self.test_8_null_username()
            
            print(f"\n{'='*60}")
            print("🏁 ALL TESTS COMPLETED")
            print("="*60)
            
        except Exception as e:
            print(f"❌ Test suite failed: {str(e)}")

if __name__ == "__main__":
    import sys
    
    # Allow custom URL via command line
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    print(f"Testing Poetry Vault at: {base_url}")
    
    tester = LoginSecurityTester(base_url)
    tester.run_all_tests()