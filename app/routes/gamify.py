from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.models import User
from app.auth import get_current_active_user
from app.exceptions import DatabaseConnectionError, UnauthorizedAccessError
from app.database import streaks_collection, safe_db_operation
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter()

# Pydantic models for gamification
class UserProgress(BaseModel):
    user_id: str
    xp: int = 0
    level: int = 1
    achievements: List[str] = []
    current_theme: str = "default"
    daily_challenges_completed: List[str] = []
    last_activity: datetime = None

class Achievement(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    xp_reward: int
    requirement: Dict[str, Any]

class XPUpdate(BaseModel):
    action: str
    xp_amount: int
    description: str

# Achievement definitions
ACHIEVEMENTS = {
    "first_steps": {
        "name": "First Steps",
        "description": "Log your first mood",
        "icon": "🎯",
        "xp_reward": 50,
        "requirement": {"moods_logged": 1}
    },
    "week_warrior": {
        "name": "Week Warrior", 
        "description": "Track moods for 7 consecutive days",
        "icon": "⚔️",
        "xp_reward": 100,
        "requirement": {"daily_streak": 7}
    },
    "mood_detective": {
        "name": "Mood Detective",
        "description": "Track 10 different emotions",
        "icon": "🔍",
        "xp_reward": 75,
        "requirement": {"unique_emotions": 10}
    },
    "ai_friend": {
        "name": "AI Friend",
        "description": "Have your first chatbot conversation",
        "icon": "🤖",
        "xp_reward": 30,
        "requirement": {"ai_chats": 1}
    },
    "reflection_pro": {
        "name": "Reflection Pro",
        "description": "Write 10 detailed mood notes",
        "icon": "📝",
        "xp_reward": 80,
        "requirement": {"mood_notes": 10}
    },
    "comeback_kid": {
        "name": "Comeback Kid",
        "description": "Return after a 3+ day break",
        "icon": "🔄",
        "xp_reward": 60,
        "requirement": {"return_after_break": True}
    }
}

# XP values for different actions
XP_VALUES = {
    "mood_logged": 10,
    "mood_note_written": 5,
    "ai_chat": 15,
    "emotion_analysis": 20,
    "daily_checkin": 25,
    "forum_help": 50,
    "achievement_earned": 0  # Achievements give their own XP
}

@router.post("/streak/{user_id}")
def update_streak(user_id: str, current_user: User = Depends(get_current_active_user)):
    """Update the streak count for the specified user."""
    try:
        # Ensure user can only update their own streak
        if user_id != current_user.username:
            raise UnauthorizedAccessError("You can only update your own streak")
        
        # Check if streak exists
        user_streak = safe_db_operation(streaks_collection.find_one, {"user_id": user_id})

        if user_streak:
            new_streak = user_streak["streak"] + 1
            safe_db_operation(
                streaks_collection.update_one,
                {"user_id": user_id},
                {"$set": {"streak": new_streak}}
            )
        else:
            new_streak = 1
            safe_db_operation(streaks_collection.insert_one, {"user_id": user_id, "streak": new_streak})

        return {"user_id": user_id, "streak": new_streak, "message": "Streak updated successfully"}
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update streak: {str(e)}"
        )

# 📌 New: Fetch current streak for a student
@router.get("/streak/{user_id}")
def get_streak(user_id: str, current_user: User = Depends(get_current_active_user)):
    """Get the current streak count for the specified user."""
    try:
        # Ensure user can only access their own streak
        if user_id != current_user.username:
            raise UnauthorizedAccessError("You can only access your own streak")
        
        user_streak = safe_db_operation(streaks_collection.find_one, {"user_id": user_id}, {"_id": 0})
        if not user_streak:
            return {"user_id": user_id, "streak": 0, "message": "No streak found"}
        return user_streak
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve streak: {str(e)}"
        )

# New gamification endpoints

@router.post("/xp/add/{user_id}")
def add_xp(user_id: str, xp_update: XPUpdate, current_user: User = Depends(get_current_active_user)):
    """Add XP to user for specific action."""
    try:
        if user_id != current_user.username:
            raise UnauthorizedAccessError("You can only update your own progress")
        
        # Get or create user progress
        progress = safe_db_operation(streaks_collection.find_one, {"user_id": user_id, "type": "progress"})
        
        if not progress:
            # Create new progress record
            new_progress = {
                "user_id": user_id,
                "type": "progress",
                "xp": xp_update.xp_amount,
                "level": 1,
                "achievements": [],
                "current_theme": "default",
                "daily_challenges_completed": [],
                "last_activity": datetime.now()
            }
            safe_db_operation(streaks_collection.insert_one, new_progress)
        else:
            # Update existing progress
            new_xp = progress.get("xp", 0) + xp_update.xp_amount
            new_level = calculate_level(new_xp)
            
            safe_db_operation(
                streaks_collection.update_one,
                {"user_id": user_id, "type": "progress"},
                {
                    "$set": {
                        "xp": new_xp,
                        "level": new_level,
                        "last_activity": datetime.now()
                    }
                }
            )
        
        return {
            "user_id": user_id,
            "xp_added": xp_update.xp_amount,
            "total_xp": new_xp if not progress else progress.get("xp", 0) + xp_update.xp_amount,
            "level": new_level if not progress else calculate_level(progress.get("xp", 0) + xp_update.xp_amount),
            "message": f"Earned {xp_update.xp_amount} XP for {xp_update.description}"
        }
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add XP: {str(e)}"
        )

@router.get("/progress/{user_id}")
def get_user_progress(user_id: str, current_user: User = Depends(get_current_active_user)):
    """Get user's gamification progress."""
    try:
        if user_id != current_user.username:
            raise UnauthorizedAccessError("You can only access your own progress")
        
        progress = safe_db_operation(streaks_collection.find_one, {"user_id": user_id, "type": "progress"})
        
        if not progress:
            return {
                "user_id": user_id,
                "xp": 0,
                "level": 1,
                "achievements": [],
                "current_theme": "default",
                "daily_challenges_completed": [],
                "last_activity": None
            }
        
        # Remove MongoDB _id and type fields
        progress.pop("_id", None)
        progress.pop("type", None)
        
        return progress
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve progress: {str(e)}"
        )

@router.get("/achievements/{user_id}")
def get_user_achievements(user_id: str, current_user: User = Depends(get_current_active_user)):
    """Get user's earned achievements."""
    try:
        if user_id != current_user.username:
            raise UnauthorizedAccessError("You can only access your own achievements")
        
        progress = safe_db_operation(streaks_collection.find_one, {"user_id": user_id, "type": "progress"})
        earned_achievements = progress.get("achievements", []) if progress else []
        
        # Return achievement details
        achievements = []
        for achievement_id in earned_achievements:
            if achievement_id in ACHIEVEMENTS:
                achievements.append({
                    "id": achievement_id,
                    **ACHIEVEMENTS[achievement_id]
                })
        
        return {
            "user_id": user_id,
            "achievements": achievements,
            "total_achievements": len(achievements)
        }
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve achievements: {str(e)}"
        )

@router.post("/achievements/check/{user_id}")
def check_achievements(user_id: str, current_user: User = Depends(get_current_active_user)):
    """Check and award new achievements based on user activity."""
    try:
        if user_id != current_user.username:
            raise UnauthorizedAccessError("You can only check your own achievements")
        
        # Get user progress
        progress = safe_db_operation(streaks_collection.find_one, {"user_id": user_id, "type": "progress"})
        if not progress:
            return {"new_achievements": [], "message": "No progress found"}
        
        earned_achievements = progress.get("achievements", [])
        new_achievements = []
        
        # Check each achievement
        for achievement_id, achievement_data in ACHIEVEMENTS.items():
            if achievement_id in earned_achievements:
                continue
                
            if check_achievement_requirement(user_id, achievement_data["requirement"]):
                # Award achievement
                earned_achievements.append(achievement_id)
                new_achievements.append({
                    "id": achievement_id,
                    **achievement_data
                })
                
                # Add XP for achievement
                add_xp(user_id, XPUpdate(
                    action="achievement_earned",
                    xp_amount=achievement_data["xp_reward"],
                    description=f"Earned {achievement_data['name']} achievement"
                ), current_user)
        
        # Update achievements list
        if new_achievements:
            safe_db_operation(
                streaks_collection.update_one,
                {"user_id": user_id, "type": "progress"},
                {"$set": {"achievements": earned_achievements}}
            )
        
        return {
            "new_achievements": new_achievements,
            "total_achievements": len(earned_achievements),
            "message": f"Found {len(new_achievements)} new achievements"
        }
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check achievements: {str(e)}"
        )

# Helper functions
def calculate_level(xp: int) -> int:
    """Calculate user level based on XP."""
    if xp < 100:
        return 1
    elif xp < 300:
        return 2
    elif xp < 600:
        return 3
    elif xp < 1000:
        return 4
    elif xp < 1500:
        return 5
    else:
        return min(50, (xp // 200) + 1)

def check_achievement_requirement(user_id: str, requirement: Dict[str, Any]) -> bool:
    """Check if user meets achievement requirement."""
    # This is a simplified version - in production, you'd query actual user data
    # For now, we'll use basic checks based on available data
    
    if "moods_logged" in requirement:
        # Check mood count from moods collection
        from app.database import moods_collection
        mood_count = safe_db_operation(moods_collection.count_documents, {"user_id": user_id})
        return mood_count >= requirement["moods_logged"]
    
    if "daily_streak" in requirement:
        # Check streak from existing streak system
        streak_data = safe_db_operation(streaks_collection.find_one, {"user_id": user_id, "type": "streak"})
        if streak_data:
            return streak_data.get("streak", 0) >= requirement["daily_streak"]
        return False
    
    # Add more requirement checks as needed
    return False
