import requests
import json

def test_authentication_flow():
    """Test the complete authentication flow"""
    base_url = "http://localhost:7860"

    print("Testing authentication flow...")

    # Test 1: Try to login with a non-existent user
    print("\n1. Testing login with non-existent user:")
    login_response = requests.post(f"{base_url}/api/login",
                                  json={"email": "nonexistent@test.com", "password": "password"})
    print(f"   Status: {login_response.status_code}")
    print(f"   Response: {login_response.json()}")

    # Test 2: Register a new user
    print("\n2. Registering a new user:")
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword123",
        "name": "Test User"
    }

    register_response = requests.post(f"{base_url}/api/register", json=user_data)
    print(f"   Status: {register_response.status_code}")

    if register_response.status_code == 200:
        print("   Registration successful!")
        print(f"   Response keys: {list(register_response.json().keys())}")

        # Test 3: Login with the newly created user
        print("\n3. Logging in with the new user:")
        login_data = {
            "email": "testuser@example.com",
            "password": "securepassword123"
        }

        login_response = requests.post(f"{base_url}/api/login", json=login_data)
        print(f"   Status: {login_response.status_code}")

        if login_response.status_code == 200:
            print("   ✓ Login successful!")
            response_data = login_response.json()
            print(f"   Has access_token: {'access_token' in response_data}")
            print(f"   Token type: {response_data.get('token_type', 'Not found')}")
        else:
            print(f"   ✗ Login failed: {login_response.json()}")

    elif register_response.status_code == 400 and "already registered" in register_response.json().get('detail', ''):
        print("   User already exists, proceeding to login test...")

        # Try to login with existing user
        print("\n3. Logging in with existing user:")
        login_data = {
            "email": "testuser@example.com",
            "password": "securepassword123"
        }

        login_response = requests.post(f"{base_url}/api/login", json=login_data)
        print(f"   Status: {login_response.status_code}")

        if login_response.status_code == 200:
            print("   ✓ Login successful!")
            response_data = login_response.json()
            print(f"   Has access_token: {'access_token' in response_data}")
            print(f"   Token type: {response_data.get('token_type', 'Not found')}")
        else:
            print(f"   ✗ Login failed: {login_response.json()}")
    else:
        print(f"   Registration failed: {register_response.json()}")

    # Test 4: Try to login with wrong password
    print("\n4. Testing login with wrong password:")
    wrong_login_data = {
        "email": "testuser@example.com",
        "password": "wrongpassword"
    }

    wrong_login_response = requests.post(f"{base_url}/api/login", json=wrong_login_data)
    print(f"   Status: {wrong_login_response.status_code}")
    if wrong_login_response.status_code == 401:
        print("   ✓ Correctly rejected wrong password")
    else:
        print(f"   ✗ Unexpected response for wrong password: {wrong_login_response.json()}")

    print("\nAuthentication flow test completed!")

if __name__ == "__main__":
    test_authentication_flow()