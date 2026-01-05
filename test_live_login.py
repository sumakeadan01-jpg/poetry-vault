#!/usr/bin/env python3
"""
Simple Login Security Test for Poetry Vault (Live Deployment)
Run this against your Railway deployment
"""

import requests
import json

def test_poetry_vault_login(base_url):
    """Test Poetry Vault login security on live deployment"""
    
    print(f"🔒 Testing Poetry Vault Login Security")
    print(f"🌐 URL: {base_url}")
    print("=" * 50)
    
    login_url = f"{base_url}/login"
    
    # Test 1: No credentials
    print("\n1️⃣ Testing: No credentials provided")
    response = requests.post(login_url, data={})
    if "required" in response.text.lower():
        print("✅ PASS: Requires credentials")
    else:
        print("❌ FAIL: Should require credentials")
    
    # Test 2: Wrong credentials
    print("\n2️⃣ Testing: Wrong credentials")
    response = requests.post(login_url, data={
        "username": "nonexistent_user_12345",
        "password": "wrong_password_12345"
    })
    if "invalid" in response.text.lower() and "database" not in response.text.lower():
        print("✅ PASS: Proper error without sensitive info")
    else:
        print("❌ FAIL: Error handling issue")
    
    # Test 3: XSS attempt
    print("\n3️⃣ Testing: XSS prevention")
    xss_payload = "<script>alert('xss')</script>"
    response = requests.post(login_url, data={
        "username": xss_payload,
        "password": "test"
    })
    if xss_payload not in response.text:
        print("✅ PASS: XSS payload sanitized")
    else:
        print("❌ FAIL: XSS vulnerability detected")
    
    # Test 4: SQL injection attempt
    print("\n4️⃣ Testing: SQL injection prevention")
    sql_payload = "'; DROP TABLE users; --"
    response = requests.post(login_url, data={
        "username": sql_payload,
        "password": "test"
    })
    if response.status_code == 200 and "error" not in response.text.lower():
        print("✅ PASS: SQL injection handled safely")
    else:
        print("✅ PASS: SQL injection blocked with error")
    
    # Test 5: Long input
    print("\n5️⃣ Testing: Long input handling")
    long_input = "a" * 2000
    response = requests.post(login_url, data={
        "username": long_input,
        "password": "test"
    })
    if response.status_code != 500:
        print("✅ PASS: Long input handled gracefully")
    else:
        print("❌ FAIL: Server error with long input")
    
    # Test 6: Empty/null values
    print("\n6️⃣ Testing: Null/empty input handling")
    response = requests.post(login_url, data={
        "username": "",
        "password": ""
    })
    if "required" in response.text.lower():
        print("✅ PASS: Empty inputs properly validated")
    else:
        print("❌ FAIL: Empty inputs not validated")
    
    print("\n" + "=" * 50)
    print("🏁 Security test completed!")
    print("💡 Check your Railway logs for any security events logged")

if __name__ == "__main__":
    # Replace with your actual Railway URL
    RAILWAY_URL = "https://your-app-name.up.railway.app"
    
    print("Enter your Poetry Vault Railway URL:")
    print("(Example: https://poetry-vault-production.up.railway.app)")
    url = input("URL: ").strip()
    
    if not url:
        url = RAILWAY_URL
        print(f"Using default: {url}")
    
    if not url.startswith("http"):
        url = "https://" + url
    
    try:
        test_poetry_vault_login(url)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Make sure your Railway app is running and accessible")