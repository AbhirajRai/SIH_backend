#!/usr/bin/env python3
"""
Test MongoDB connection with different approaches
"""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError
import socket
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import MONGODB_URL

def test_dns_resolution():
    """Test DNS resolution for MongoDB cluster."""
    print("🔍 Testing DNS resolution...")
    
    try:
        # Extract hostname from MongoDB URL
        hostname = "mindcareluster.ftrolml.mongodb.net"
        print(f"Resolving hostname: {hostname}")
        
        ip_addresses = socket.getaddrinfo(hostname, 27017, socket.AF_INET)
        print(f"✅ DNS resolution successful: {ip_addresses[0][4][0]}")
        return True
    except Exception as e:
        print(f"❌ DNS resolution failed: {e}")
        return False

def test_mongodb_connection_basic():
    """Test basic MongoDB connection."""
    print("\n🔍 Testing basic MongoDB connection...")
    
    try:
        client = MongoClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ Basic MongoDB connection successful")
        client.close()
        return True
    except Exception as e:
        print(f"❌ Basic MongoDB connection failed: {e}")
        return False

def test_mongodb_connection_extended():
    """Test MongoDB connection with extended timeout."""
    print("\n🔍 Testing MongoDB connection with extended timeout...")
    
    try:
        client = MongoClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=30000,  # 30 seconds
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            retryWrites=True,
            maxPoolSize=10,
            retryReads=True
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ Extended MongoDB connection successful")
        
        # Test database access
        db = client["mindcare"]
        collections = db.list_collection_names()
        print(f"✅ Database access successful. Collections: {collections}")
        
        client.close()
        return True
    except Exception as e:
        print(f"❌ Extended MongoDB connection failed: {e}")
        return False

def test_mongodb_connection_alternative():
    """Test MongoDB connection with alternative settings."""
    print("\n🔍 Testing MongoDB connection with alternative settings...")
    
    try:
        # Try with different connection options
        client = MongoClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=15000,
            connectTimeoutMS=15000,
            socketTimeoutMS=15000,
            retryWrites=True,
            maxPoolSize=5,
            retryReads=True,
            maxIdleTimeMS=30000,
            waitQueueTimeoutMS=10000,
            heartbeatFrequencyMS=10000
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ Alternative MongoDB connection successful")
        
        # Test database access
        db = client["mindcare"]
        users_collection = db["users"]
        
        # Test a simple query
        count = users_collection.count_documents({})
        print(f"✅ Database query successful. Users count: {count}")
        
        client.close()
        return True
    except Exception as e:
        print(f"❌ Alternative MongoDB connection failed: {e}")
        return False

def test_network_connectivity():
    """Test general network connectivity."""
    print("\n🔍 Testing network connectivity...")
    
    try:
        # Test if we can reach external services
        import urllib.request
        response = urllib.request.urlopen('https://www.google.com', timeout=10)
        print("✅ General network connectivity working")
        return True
    except Exception as e:
        print(f"❌ Network connectivity issue: {e}")
        return False

def main():
    """Run all MongoDB connection tests."""
    print("🧪 MongoDB Connection Diagnostic Tool")
    print("=" * 50)
    
    tests = [
        ("DNS Resolution", test_dns_resolution),
        ("Network Connectivity", test_network_connectivity),
        ("Basic MongoDB Connection", test_mongodb_connection_basic),
        ("Extended MongoDB Connection", test_mongodb_connection_extended),
        ("Alternative MongoDB Connection", test_mongodb_connection_alternative),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MongoDB connection should work.")
    else:
        print("⚠️  Some tests failed. Check the results above for specific issues.")

if __name__ == "__main__":
    main()
