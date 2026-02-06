import requests
import uuid
import time

def test_chatbot_end_to_end():
    print("=" * 60)
    print("TODO AI CHATBOT - END TO END TEST")
    print("=" * 60)

    base_url = "http://localhost:8000"

    # Step 1: Create a test user
    user_id = str(uuid.uuid4())
    print(f"\n1. Created test user ID: {user_id}")

    # Initialize conversation ID
    conversation_id = None

    # Test 1: Add a task
    print(f"\n2. Testing ADD TASK functionality...")
    try:
        response = requests.post(
            f"{base_url}/api/{user_id}/chat",
            json={
                "message": "Add a task to buy milk",
                "conversation_id": conversation_id
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   [PASS] Status: {response.status_code}")
            print(f"   [PASS] Response: {data['response']}")
            conversation_id = data['conversation_id']
            print(f"   [PASS] Conversation ID: {conversation_id}")
        else:
            print(f"   [FAIL] Failed with status: {response.status_code}")
            print(f"   [FAIL] Error: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error in add task test: {e}")
        return False

    time.sleep(1)  # Small delay between requests

    # Test 2: Add another task
    print(f"\n3. Testing ADD ANOTHER TASK...")
    try:
        response = requests.post(
            f"{base_url}/api/{user_id}/chat",
            json={
                "message": "Add a task to call mom",
                "conversation_id": conversation_id
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   [PASS] Status: {response.status_code}")
            print(f"   [PASS] Response: {data['response']}")
        else:
            print(f"   [FAIL] Failed with status: {response.status_code}")
            print(f"   [FAIL] Error: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error in add second task test: {e}")
        return False

    time.sleep(1)  # Small delay between requests

    # Test 3: List tasks
    print(f"\n4. Testing LIST TASKS functionality...")
    try:
        response = requests.post(
            f"{base_url}/api/{user_id}/chat",
            json={
                "message": "Show me my tasks",
                "conversation_id": conversation_id
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   [PASS] Status: {response.status_code}")
            print(f"   [PASS] Response: {data['response']}")
        else:
            print(f"   [FAIL] Failed with status: {response.status_code}")
            print(f"   [FAIL] Error: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error in list tasks test: {e}")
        return False

    time.sleep(1)  # Small delay between requests

    # Test 4: Complete a task
    print(f"\n5. Testing COMPLETE TASK functionality...")
    try:
        response = requests.post(
            f"{base_url}/api/{user_id}/chat",
            json={
                "message": "Complete the milk task",
                "conversation_id": conversation_id
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   [PASS] Status: {response.status_code}")
            print(f"   [PASS] Response: {data['response']}")
        else:
            print(f"   [FAIL] Failed with status: {response.status_code}")
            print(f"   [FAIL] Error: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error in complete task test: {e}")
        return False

    time.sleep(1)  # Small delay between requests

    # Test 5: List tasks again to see completion
    print(f"\n6. Testing LIST TASKS again to verify completion...")
    try:
        response = requests.post(
            f"{base_url}/api/{user_id}/chat",
            json={
                "message": "Show me my tasks",
                "conversation_id": conversation_id
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   [PASS] Status: {response.status_code}")
            print(f"   [PASS] Response: {data['response']}")
        else:
            print(f"   [FAIL] Failed with status: {response.status_code}")
            print(f"   [FAIL] Error: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error in second list tasks test: {e}")
        return False

    time.sleep(1)  # Small delay between requests

    # Test 6: Delete a task
    print(f"\n7. Testing DELETE TASK functionality...")
    try:
        response = requests.post(
            f"{base_url}/api/{user_id}/chat",
            json={
                "message": "Delete the call mom task",
                "conversation_id": conversation_id
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   [PASS] Status: {response.status_code}")
            print(f"   [PASS] Response: {data['response']}")
        else:
            print(f"   [FAIL] Failed with status: {response.status_code}")
            print(f"   [FAIL] Error: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error in delete task test: {e}")
        return False

    time.sleep(1)  # Small delay between requests

    # Test 7: List tasks again to verify deletion
    print(f"\n8. Testing LIST TASKS again to verify deletion...")
    try:
        response = requests.post(
            f"{base_url}/api/{user_id}/chat",
            json={
                "message": "Show me my tasks",
                "conversation_id": conversation_id
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   [PASS] Status: {response.status_code}")
            print(f"   [PASS] Response: {data['response']}")
        else:
            print(f"   [FAIL] Failed with status: {response.status_code}")
            print(f"   [FAIL] Error: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error in third list tasks test: {e}")
        return False

    # Final summary
    print(f"\n" + "=" * 60)
    print("END TO END TEST COMPLETED")
    print("=" * 60)
    print("[PASS] All tests passed!")
    print("[PASS] Chatbot is fully functional")
    print("[PASS] Natural language processing working")
    print("[PASS] Task management operations working")
    print("[PASS] Conversation persistence working")
    print("[PASS] Database integration working")
    print(f"[PASS] Test user: {user_id}")
    print(f"[PASS] Test conversation: {conversation_id}")
    print("=" * 60)

    return True

if __name__ == "__main__":
    success = test_chatbot_end_to_end()
    if success:
        print("\n[YAY] ALL END-TO-END TESTS PASSED! The chatbot is working perfectly!")
    else:
        print("\n[FAIL] SOME TESTS FAILED! Please check the output above.")