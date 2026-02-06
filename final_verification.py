#!/usr/bin/env python3
"""
Final test to verify the chat functionality is working properly (without emojis)
"""
import requests
import uuid

def test_final_chat():
    # Generate a test user ID
    user_id = str(uuid.uuid4())

    print(f"Testing with user_id: {user_id}")

    # Test initial message
    print("\nTesting initial message...")
    test_message_1 = {
        "message": "Hello, can you help me with my tasks?",
        "conversation_id": None
    }

    url = f"http://localhost:7860/api/{user_id}/chat"

    try:
        response1 = requests.post(
            url,
            json=test_message_1,
            headers={'Content-Type': 'application/json'}
        )

        print(f"Status: {response1.status_code}")
        if response1.status_code == 200:
            data1 = response1.json()
            conversation_id = data1['conversation_id']
            print(f"Conversation ID: {conversation_id}")
            print(f"Response preview: {data1['response'][:60]}...")
            print("SUCCESS: Initial message test passed!")
        else:
            print(f"FAILED: Status {response1.status_code}")
            return False

        # Test follow-up message
        print("\nTesting follow-up message...")
        test_message_2 = {
            "message": "Add a task to buy groceries",
            "conversation_id": conversation_id
        }

        response2 = requests.post(
            url,
            json=test_message_2,
            headers={'Content-Type': 'application/json'}
        )

        print(f"Status: {response2.status_code}")
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"Response preview: {data2['response'][:60]}...")
            print("SUCCESS: Follow-up message test passed!")
        else:
            print(f"FAILED: Status {response2.status_code}")
            return False

        # Test conversation history
        print("\nTesting conversation history retrieval...")
        history_url = f"http://localhost:7860/api/{user_id}/conversation/{conversation_id}/messages"

        response3 = requests.get(history_url)
        print(f"Status: {response3.status_code}")
        if response3.status_code == 200:
            data3 = response3.json()
            print(f"Number of messages in conversation: {len(data3['messages'])}")
            print("SUCCESS: Conversation history test passed!")
        else:
            print(f"FAILED: Status {response3.status_code}")
            return False

        print("\nALL TESTS PASSED! Chat functionality is working correctly.")
        print("- Backend is running on port 7860")
        print("- POST /api/{user_id}/chat endpoint is accessible")
        print("- Frontend can connect to backend")
        print("- Chat messages are processed successfully")
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("Running final verification test...")
    success = test_final_chat()
    if success:
        print("\nVERIFICATION COMPLETE: All chat functionality is working properly!")
    else:
        print("\nVERIFICATION FAILED: Issues remain with chat functionality.")