#!/usr/bin/env python3
"""
Quick Poetry Vault Test - Verify your deployment is working
"""

import requests

def test_poetry_vault():
    base_url = "https://web-production-2c42e.up.railway.app"
    
    print("🔍 Testing Poetry Vault Deployment")
    print("=" * 40)
    
    # Test 1: Check if site is accessible
    print("\n1️⃣ Testing site accessibility...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Site is accessible")
        else:
            print(f"❌ Site returned status: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to site: {e}")
        return
    
    # Test 2: Check login page
    print("\n2️⃣ Testing login page...")
    login_response = requests.get(f"{base_url}/login")
    if login_response.status_code == 200 and "login" in login_response.text.lower():
        print("✅ Login page accessible")
    else:
        print("❌ Login page issue")
    
    # Test 3: Test form-based login with invalid credentials
    print("\n3️⃣ Testing login form with invalid credentials...")
    login_data = {
        "username": "test_invalid_user_12345",
        "password": "wrong_password_12345"
    }
    
    login_post = requests.post(f"{base_url}/login", data=login_data)
    if login_post.status_code == 200 and ("invalid" in login_post.text.lower() or "error" in login_post.text.lower()):
        print("✅ Login form properly rejects invalid credentials")
    else:
        print("❌ Login form validation issue")
    
    # Test 4: Test empty credentials
    print("\n4️⃣ Testing empty credentials...")
    empty_data = {"username": "", "password": ""}
    empty_response = requests.post(f"{base_url}/login", data=empty_data)
    if empty_response.status_code == 200 and "required" in empty_response.text.lower():
        print("✅ Empty credentials properly validated")
    else:
        print("❌ Empty credential validation issue")
    
    # Test 5: Test feedback page
    print("\n5️⃣ Testing feedback page...")
    feedback_response = requests.get(f"{base_url}/feedback")
    if feedback_response.status_code == 200 and "feedback" in feedback_response.text.lower():
        print("✅ Feedback page accessible")
    else:
        print("❌ Feedback page issue")
    
    # Test 6: Test XSS protection
    print("\n6️⃣ Testing XSS protection...")
    xss_data = {
        "username": "<script>alert('xss')</script>",
        "password": "test"
    }
    xss_response = requests.post(f"{base_url}/login", data=xss_data)
    if "<script>" not in xss_response.text:
        print("✅ XSS protection working")
    else:
        print("❌ XSS vulnerability detected")
    
    print("\n" + "=" * 40)
    print("🎉 Poetry Vault deployment test completed!")
    print("💡 Your app uses HTML forms, not JSON API")

if __name__ == "__main__":
    test_poetry_vault()