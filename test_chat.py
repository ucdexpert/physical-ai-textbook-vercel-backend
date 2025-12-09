import requests
import sys

def test_health():
    url = "http://127.0.0.1:8001/health"
    print("Checking health...")
    try:
        response = requests.get(url, timeout=5)
        print(f"Health Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return False
    return True

def test_chat():
    url = "http://127.0.0.1:8001/chat"
    payload = {"query": "What is ROS 2?"}
    print("Testing chat...")
    try:
        response = requests.post(url, json=payload, timeout=60)
        print(f"Chat Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Chat Test Failed: {e}")

if __name__ == "__main__":
    if test_health():
        test_chat()
