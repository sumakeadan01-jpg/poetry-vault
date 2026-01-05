#!/usr/bin/env python3
"""
Correct Login Tests for Poetry Vault
Your app uses HTML forms, not JSON API
"""

import requests
import re

def test_valid_login():
    """Test with valid credentials (you need to create a test user first)"""
    url = "https://web-production-2c42e.up.railway.app/login"
    
    # Use form data, not JSON
    credentials = {
        "username": "test_user",  # Replace with actual test user
        "password": "test_password"  # Replace with actual password
    }
    
    response = requests.post(url, data=credentials)  # data, not json
    
    print("Response Status Code:", response.status_code)
    print("Response URL:", response.url)
    
    # For successful login, expect redirect (302) or success page (200)
    if response.status_code == 200:
        if "home" in response.text.lower() or "welcome" in response.text.lower():
            print("✅ PASS: Login successful")
        else:
            print("❌ FAIL: Login failed")
    elif response.status_code == 302:
        print("✅ PASS: Login successful (redirected)")
    else:
        print(f"❌ FAIL: Unexpected status code: {response.status_code}")

def test_invalid_login():
    """Test with invalid credentials"""
    url = "https://web-production-2c42e.up.railway.app/login"
    
    payload = {
        "username": "nonexistent_user_12345",
        "password": "wrong_password_12345"
    }
    
    response = requests.post(url, data=payload)  # data, not json
    
    print("Response Code:", response.status_code)
    print("Response contains error:", "invalid" in response.text.lower())
    
    # Poetry Vault returns HTML with error message, not JSON
    if response.status_code == 200 and "invalid" in response.text.lower():
        print("✅ PASS: Invalid login properly rejected")
    else:
        print("❌ FAIL: Invalid login not handled correctly")

def test_empty_credentials():
    """Test with empty credentials"""
    url = "https://web-production-2c42e.up.railway.app/login"
    
    payload = {
        "username": "",
        "password": ""
    }
    
    response = requests.post(url, data=payload)  # data, not json
    
    print(f"Response Status Code: {response.status_code}")
    print(f"Contains 'required': {'required' in response.text.lower()}")
    
    # Should return HTML page with error message
    if response.status_code == 200 and "required" in response.text.lower():
        print("✅ PASS: Empty credentials properly validated")
    else:
        print("❌ FAIL: Empty credentials not validated")

def test_long_input_validation():
    """Test with very long input"""
    url = "https://web-production-2c42e.up.railway.app/login"
    
    credentials = {
        "username": "a" * 2000,  # Very long username
        "password": "b" * 2000   # Very long password
    }
    
    response = requests.post(url, data=credentials)  # data, not json
    
    print(f"Response Status Code: {response.status_code}")
    
    # Should handle gracefully without server error
    if response.status_code != 500:
        print("✅ PASS: Long input handled gracefully")
    else:
        print("❌ FAIL: Server error with long input")

def test_xss_prevention():
    """Test XSS prevention"""
    url = "https://web-production-2c42e.up.railway.app/login"
    
    xss_payload = "<script>alert('xss')</script>"
    
    credentials = {
        "username": xss_payload,
        "password": "test_password"
    }
    
    response = requests.post(url, data=credentials)  # data, not json
    
    print(f"Response Status Code: {response.status_code}")
    print(f"XSS payload reflected: {xss_payload in response.text}")
    
    # XSS payload should be sanitized
    if xss_payload not in response.text:
        print("✅ PASS: XSS payload properly sanitized")
    else:
        print("❌ FAIL: XSS vulnerability detected")

def test_sql_injection_prevention():
    """Test SQL injection prevention"""
    url = "https://web-production-2c42e.up.railway.app/login"
    
    sql_payload = "'; DROP TABLE users; --"
    
    credentials = {
        "username": sql_payload,
        "password": "test_password"
    }
    
    response = requests.post(url, data=credentials)  # data, not json
    
    print(f"Response Status Code: {response.status_code}")
    
    # Should handle safely without database errors
    if response.status_code == 200:
        print("✅ PASS: SQL injection handled safely")
    else:
        print("⚠️  WARNING: Unexpected response to SQL injection attempt")

def run_all_tests():
    """Run all corrected tests"""
    print("🔒 POETRY VAULT LOGIN TESTS (Corrected for HTML Forms)")
    print("=" * 60)
    
    print("\n1️⃣ Testing Valid Login (create test user first)")
    test_valid_login()
    
    print("\n2️⃣ Testing Invalid Login")
    test_invalid_login()
    
    print("\n3️⃣ Testing Empty Credentials")
    test_empty_credentials()
    
    print("\n4️⃣ Testing Long Input Validation")
    test_long_input_validation()
    
    print("\n5️⃣ Testing XSS Prevention")
    test_xss_prevention()
    
    print("\n6️⃣ Testing SQL Injection Prevention")
    test_sql_injection_prevention()
    
    print("\n" + "=" * 60)
    print("🏁 ALL TESTS COMPLETED")
    print("💡 Note: Poetry Vault uses HTML forms, not JSON API")

if __name__ == "__main__":
    run_all_tests()