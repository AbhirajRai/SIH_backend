from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson import ObjectId
from datetime import datetime
from app.models import MoodLog, User
from app.auth import get_current_active_user
from app.exceptions import DatabaseConnectionError, UnauthorizedAccessError
from app.database import moods_collection, safe_db_operation

router = APIRouter()

# 📌 POST - Log a new mood
@router.post("/")
def log_mood(mood: MoodLog, current_user: User = Depends(get_current_active_user)):
    """Log a new mood entry for the current user."""
    try:
        # Ensure user can only log moods for themselves
        if mood.user_id != current_user.username:
            raise UnauthorizedAccessError("You can only log moods for yourself")
        
        # Add timestamp to mood data
        mood_data = mood.dict()
        mood_data["timestamp"] = datetime.utcnow()
        
        if moods_collection is None:
            print("❌ Moods collection is None - database not connected")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database not connected"
            )
        
        result = safe_db_operation(moods_collection.insert_one, mood_data)
        return {
            "message": "Mood logged successfully ✅", 
            "id": str(result.inserted_id), 
            "data": mood
        }
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log mood: {str(e)}"
        )

# 📌 GET - Fetch all moods for a student
@router.get("/{user_id}")
def get_mood_history(user_id: str, current_user: User = Depends(get_current_active_user)):
    """Get mood history for the specified user."""
    try:
        print(f"🔍 Getting mood history for user_id: {user_id}")
        print(f"🔍 Current user: {current_user.username}")
        
        # Ensure user can only access their own mood history
        if user_id != current_user.username:
            print(f"❌ User mismatch: requested {user_id}, authenticated {current_user.username}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own mood history"
            )
        
        print(f"🔍 Querying database for user: {user_id}")
        if moods_collection is None:
            print("❌ Moods collection is None - database not connected")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database not connected"
            )
        
        moods = list(safe_db_operation(moods_collection.find, {"user_id": user_id}))
        print(f"🔍 Found {len(moods)} mood entries")
        
        # Convert ObjectId to string for JSON serialization
        for mood in moods:
            if '_id' in mood:
                mood['_id'] = str(mood['_id'])
            if 'timestamp' in mood:
                mood['timestamp'] = mood['timestamp'].isoformat()
        
        return {"user_id": user_id, "history": moods, "count": len(moods)}
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        print("❌ Database connection failed")
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        print(f"❌ Error getting mood history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve mood history: {str(e)}"
        )

# 📌 DELETE - Delete a mood log
@router.delete("/{mood_id}")
def delete_mood_log(mood_id: str, current_user: User = Depends(get_current_active_user)):
    """Delete a specific mood log entry for the current user."""
    try:
        # Validate ObjectId format
        try:
            object_id = ObjectId(mood_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid mood ID format"
            )
        
        # First, check if the mood log exists and belongs to the current user
        mood_log = safe_db_operation(moods_collection.find_one, {"_id": object_id})
        
        if not mood_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mood log not found"
            )
        
        # Ensure user can only delete their own mood logs
        if mood_log.get("user_id") != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own mood logs"
            )
        
        # Delete the mood log
        result = safe_db_operation(moods_collection.delete_one, {"_id": object_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mood log not found"
            )
        
        return {
            "message": "Mood log deleted successfully ✅",
            "deleted_id": mood_id
        }
        
    except HTTPException:
        raise
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete mood log: {str(e)}"
        )
