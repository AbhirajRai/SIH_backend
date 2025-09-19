#!/usr/bin/env python3
"""
Test database connection
"""

from app.database import connect_to_database, test_connection, users_collection
from config import MONGODB_URL

def test_database():
    """Test database connection and collections."""
    print("🔍 Testing database connection...")
    print(f"MongoDB URL: {MONGODB_URL[:50]}...")
    
    # Test connection
    if connect_to_database():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")
        return False
    
    # Test collections
    if users_collection is not None:
        print("✅ Users collection initialized")
    else:
        print("❌ Users collection is None")
        return False
    
    # Test database operation
    try:
        result = users_collection.find_one({"username": "test"})
        print("✅ Database query successful")
        return True
    except Exception as e:
        print(f"❌ Database query failed: {e}")
        return False

if __name__ == "__main__":
    test_database()
