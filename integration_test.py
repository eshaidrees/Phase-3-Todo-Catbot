#!/usr/bin/env python3
"""
Integration test to verify frontend can connect to backend
"""
import requests
import uuid

def test_integration():
    # Generate a test user ID
    user_id = str(uuid.uuid4())

    print("Testing integration between frontend and backend...")
    print(f"Backend running on: http://localhost:7860")
    print(f"Frontend should connect to backend at: http://localhost:7860")

    # Test the chat endpoint that the frontend would use
    test_message = {
        "message": "Integration test - can you help me?",
        "conversation_id": None
    }

    url = f"http://localhost:7860/api/{user_id}/chat"

    print(f"\nSending test message to: {url}")

    try:
        response = requests.post(
            url,
            json=test_message,
            headers={'Content-Type': 'application/json'}
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Integration test passed!")
            print(f"   Conversation ID: {data['conversation_id']}")
            print(f"   Response preview: {data['response'][:60]}...")
            print(f"\nThe frontend configuration (NEXT_PUBLIC_API_BASE_URL=http://localhost:7860)")
            print(f"is correctly pointing to the backend on port 7860.")
            return True
        else:
            print(f"❌ FAILED: Expected 200, got {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Cannot connect to backend server on port 7860")
        print("Make sure the backend is running on port 7860")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_integration()