import requests
import sys

def test_backend_connection():
    """Test if the backend server is accessible"""
    base_url = "http://localhost:7860"

    try:
        # Test the root endpoint
        response = requests.get(base_url)
        print(f"✓ Backend server is accessible")
        print(f"Response: {response.json()}")

        # Test the API endpoints
        auth_endpoints = [
            f"{base_url}/api/register",
            f"{base_url}/api/login"
        ]

        for endpoint in auth_endpoints:
            try:
                # We expect a 422 error for missing data, but not a connection error
                response = requests.post(endpoint, json={})
                if response.status_code in [422, 400, 401]:
                    print(f"✓ Endpoint {endpoint} is accessible (expected error for missing data)")
                else:
                    print(f"? Endpoint {endpoint} returned unexpected status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"✗ Endpoint {endpoint} is not accessible: {e}")

        return True

    except requests.exceptions.ConnectionError:
        print("✗ Backend server is not running or not accessible at http://localhost:7860")
        print("Please start the backend server with: cd backend && python main.py")
        return False
    except Exception as e:
        print(f"✗ Error testing backend connection: {e}")
        return False

if __name__ == "__main__":
    test_backend_connection()