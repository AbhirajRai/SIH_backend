#!/usr/bin/env python3
"""
Test network access from different IPs
"""

import requests
import socket
import subprocess
import json

def get_local_ip():
    """Get local IP address."""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def test_network_access():
    """Test server accessibility from different IPs."""
    print("🌐 Network Access Test")
    print("=" * 50)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"📍 Local IP: {local_ip}")
    
    # Test URLs
    test_urls = [
        "http://127.0.0.1:8000/",
        "http://localhost:8000/",
        f"http://{local_ip}:8000/",
        "http://0.0.0.0:8000/"
    ]
    
    print("\n🔍 Testing server accessibility:")
    print("-" * 30)
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {url} - OK")
            else:
                print(f"❌ {url} - Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {url} - Connection refused")
        except requests.exceptions.Timeout:
            print(f"⏰ {url} - Timeout")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
    
    print(f"\n📋 Access Information:")
    print(f"   • Server runs on: 0.0.0.0:8000")
    print(f"   • Local access: http://localhost:8000")
    print(f"   • Network access: http://{local_ip}:8000")
    print(f"   • External access: http://[YOUR_EXTERNAL_IP]:8000")
    
    print(f"\n🔧 Network Configuration:")
    print(f"   • CORS: Allow all origins (*)")
    print(f"   • Host: 0.0.0.0 (all interfaces)")
    print(f"   • Port: 8000")
    
    print(f"\n💡 To access from other devices:")
    print(f"   1. Find your external IP: https://whatismyipaddress.com/")
    print(f"   2. Use: http://[EXTERNAL_IP]:8000")
    print(f"   3. Make sure firewall allows port 8000")

def check_firewall():
    """Check Windows firewall status."""
    print("\n🔥 Firewall Check:")
    print("-" * 20)
    
    try:
        # Check if Windows Firewall is running
        result = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles", "state"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "ON" in result.stdout:
            print("⚠️  Windows Firewall is ON")
            print("💡 You may need to allow port 8000 through firewall")
            print("   Run as Administrator: netsh advfirewall firewall add rule name=\"MindCare API\" dir=in action=allow protocol=TCP localport=8000")
        else:
            print("✅ Windows Firewall is OFF")
            
    except Exception as e:
        print(f"❌ Could not check firewall: {e}")

if __name__ == "__main__":
    test_network_access()
    check_firewall()
