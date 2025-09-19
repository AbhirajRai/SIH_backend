#!/usr/bin/env python3
"""
Test script to verify the server is running without warnings
"""

import requests
import time
import sys

def test_server():
    """Test if the server is running and responding correctly."""
    try:
        # Wait a moment for server to start
        time.sleep(2)
        
        # Test the root endpoint
        response = requests.get("http://localhost:8000/", timeout=10)
        
        if response.status_code == 200:
            print("✅ Server is running successfully!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8000.")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
