#!/usr/bin/env python3
"""
Simple test server to debug mood history issues
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson import ObjectId
from datetime import datetime
import os
import warnings
from dotenv import load_dotenv  # Add this import

# Suppress warnings
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

# Load environment variables from .env file
load_dotenv()

# Get allowed origins from environment or use provided URLs
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS")
if not ALLOWED_ORIGINS or ALLOWED_ORIGINS == "*":
    ALLOWED_ORIGINS = [
        "https://sih-frontend-fw94ep52t-abhirajrais-projects.vercel.app",
        "https://sih-backend-bcnq.onrender.com"
    ]
else:
    ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

app = FastAPI(title="Simple MindCare Test", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Database connection
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb+srv://mindcare_user:IrmKVH96TWThI26J@mindcareluster.ftrolml.mongodb.net/?retryWrites=true&w=majority&appName=MindCareluster"
)

try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client["mindcare"]
    moods_collection = db["moods"]
    users_collection = db["users"]
    print("✅ Database connected successfully")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    moods_collection = None
    users_collection = None

@app.get("/")
def root():
    return {"message": "Simple MindCare API is running 🚀"}

@app.get("/moods/{user_id}")
def get_mood_history(user_id: str):
    """Get mood history for a user (simplified version)."""
    try:
        if not moods_collection:
            raise HTTPException(status_code=500, detail="Database not connected")
        
        print(f"🔍 Getting mood history for user: {user_id}")
        moods = list(moods_collection.find({"user_id": user_id}))
        print(f"🔍 Found {len(moods)} mood entries")
        
        # Convert ObjectId to string for JSON serialization
        for mood in moods:
            if '_id' in mood:
                mood['_id'] = str(mood['_id'])
            if 'timestamp' in mood:
                mood['timestamp'] = mood['timestamp'].isoformat()
        
        return {"user_id": user_id, "history": moods, "count": len(moods)}
        
    except Exception as e:
        print(f"❌ Error getting mood history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve mood history: {str(e)}"
        )

@app.post("/moods/")
def log_mood(mood_data: dict):
    """Log a new mood entry (simplified version)."""
    try:
        if not moods_collection:
            raise HTTPException(status_code=500, detail="Database not connected")
        
        print(f"🔍 Logging mood: {mood_data}")
        mood_data["timestamp"] = datetime.utcnow()
        
        result = moods_collection.insert_one(mood_data)
        return {
            "message": "Mood logged successfully ✅", 
            "id": str(result.inserted_id), 
            "data": mood_data
        }
        
    except Exception as e:
        print(f"❌ Error logging mood: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to log mood: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting simple test server...")
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "info")
    )