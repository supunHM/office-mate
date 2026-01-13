"""
Simple test script for authentication API
"""
import requests
import json

BASE_URL = 'http://localhost:5001'

print("Testing Flask Authentication API")
print("=" * 60)

# Test 1: Register user
print("\n1. Testing User Registration")
print("-" * 60)

data = {
    "username": "Supun",
    "email": "supun@gmail.com",
    "password": "Supun123",
    "full_name": "supun madhuwantha"
}

try:
    response = requests.post(f'{BASE_URL}/api/auth/register', json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("\n✅ Registration successful!")
        access_token = response.json().get('access_token')
        
        # Test 2: Get current user
        print("\n2. Testing Get Current User (Protected Route)")
        print("-" * 60)
        headers = {'Authorization': f'Bearer {access_token}'}
        me_response = requests.get(f'{BASE_URL}/api/auth/me', headers=headers)
        print(f"Status Code: {me_response.status_code}")
        print(f"Response: {json.dumps(me_response.json(), indent=2)}")
        
        # Test 3: Login
        print("\n3. Testing Login")
        print("-" * 60)
        login_data = {
            "username": "Supun",
            "password": "Supun123"
        }
        login_response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
        print(f"Status Code: {login_response.status_code}")
        print(f"Response: {json.dumps(login_response.json(), indent=2)}")
        
    elif response.status_code == 400:
        error = response.json().get('error')
        if 'already exists' in error:
            print(f"\n⚠️  User already exists. Testing login instead...")
            
            # Try login
            login_data = {
                "username": "Supun",
                "password": "Supun123"
            }
            login_response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
            print(f"Login Status Code: {login_response.status_code}")
            print(f"Login Response: {json.dumps(login_response.json(), indent=2)}")
        else:
            print(f"\n❌ Error: {error}")
            
except requests.exceptions.ConnectionError:
    print("❌ Error: Could not connect to Flask server")
    print("Please ensure the server is running: python flask_app.py")
except requests.exceptions.Timeout:
    print("❌ Error: Request timed out")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("Testing complete!")
