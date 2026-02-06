#!/usr/bin/env python3
"""
Comprehensive test to verify the chat functionality is working properly
"""
import requests
import uuid
import time

def test_comprehensive_chat():
    # Generate a test user ID
    user_id = str(uuid.uuid4())

    print(f"Testing with user_id: {user_id}")

    # Test 1: Initial message
    print("\n1. Testing initial message...")
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

        print(f"   Status: {response1.status_code}")
        if response1.status_code == 200:
            data1 = response1.json()
            conversation_id = data1['conversation_id']
            print(f"   Conversation ID: {conversation_id}")
            print(f"   Response: {data1['response'][:80]}...")
            print("   ✅ Initial message successful")
        else:
            print(f"   ❌ Failed with status {response1.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

    # Test 2: Follow-up message in same conversation
    print("\n2. Testing follow-up message in same conversation...")
    test_message_2 = {
        "message": "Add a task to buy groceries",
        "conversation_id": conversation_id
    }

    try:
        response2 = requests.post(
            url,
            json=test_message_2,
            headers={'Content-Type': 'application/json'}
        )

        print(f"   Status: {response2.status_code}")
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"   Conversation ID: {data2['conversation_id']}")
            print(f"   Response: {data2['response'][:80]}...")
            print("   ✅ Follow-up message successful")
        else:
            print(f"   ❌ Failed with status {response2.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

    # Test 3: Get conversation history
    print("\n3. Testing conversation history retrieval...")
    history_url = f"http://localhost:7860/api/{user_id}/conversation/{conversation_id}/messages"

    try:
        response3 = requests.get(history_url)

        print(f"   Status: {response3.status_code}")
        if response3.status_code == 200:
            data3 = response3.json()
            print(f"   Number of messages: {len(data3['messages'])}")
            for i, msg in enumerate(data3['messages']):
                print(f"     {i+1}. {msg['role']}: {msg['content'][:50]}...")
            print("   ✅ Conversation history retrieval successful")
        else:
            print(f"   ❌ Failed with status {response3.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

    # Test 4: List all user conversations
    print("\n4. Testing user conversations listing...")
    conv_list_url = f"http://localhost:7860/api/{user_id}/conversations"

    try:
        response4 = requests.get(conv_list_url)

        print(f"   Status: {response4.status_code}")
        if response4.status_code == 200:
            data4 = response4.json()
            print(f"   Number of conversations: {len(data4['conversations'])}")
            print("   ✅ Conversations listing successful")
        else:
            print(f"   ❌ Failed with status {response4.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

    print("\n🎉 ALL TESTS PASSED! Chat functionality is working correctly.")
    return True

if __name__ == "__main__":
    print("Running comprehensive chat functionality test...")
    test_comprehensive_chat()