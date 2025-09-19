"""
Database fallback for when MongoDB is not available
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class InMemoryDB:
    """Simple in-memory database for fallback when MongoDB is not available."""
    
    def __init__(self):
        self.users = {}
        self.moods = []
        self.chats = []
        self.streaks = {}
        logger.info("✅ In-memory database initialized")
    
    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one document matching the query."""
        if "users" in str(query):
            for user in self.users.values():
                if all(user.get(k) == v for k, v in query.items()):
                    return user
        elif "moods" in str(query):
            for mood in self.moods:
                if all(mood.get(k) == v for k, v in query.items()):
                    return mood
        return None
    
    def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find all documents matching the query."""
        results = []
        if "moods" in str(query):
            for mood in self.moods:
                if all(mood.get(k) == v for k, v in query.items()):
                    results.append(mood)
        return results
    
    def insert_one(self, document: Dict[str, Any]) -> Any:
        """Insert one document."""
        if "user_id" in document:  # Mood document
            document["_id"] = f"mood_{len(self.moods)}"
            document["timestamp"] = datetime.utcnow()
            self.moods.append(document)
            return type('Result', (), {'inserted_id': document["_id"]})()
        else:  # User document
            user_id = f"user_{len(self.users)}"
            document["_id"] = user_id
            document["created_at"] = datetime.utcnow()
            self.users[user_id] = document
            return type('Result', (), {'inserted_id': user_id})()

# Global fallback database
fallback_db = InMemoryDB()

def get_fallback_collection(collection_name: str):
    """Get a fallback collection when MongoDB is not available."""
    return fallback_db
