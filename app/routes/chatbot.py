from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
from app.models import ChatMessage, User
from app.auth import get_current_active_user
from app.exceptions import DatabaseConnectionError, UnauthorizedAccessError
from app.database import chat_collection, safe_db_operation

router = APIRouter()

@router.post("/")
def chat(msg: ChatMessage, current_user: User = Depends(get_current_active_user)):
    """Send a message to the chatbot and get a response."""
    try:
        # Ensure user can only chat for themselves
        if msg.user_id != current_user.username:
            raise UnauthorizedAccessError("You can only chat for yourself")
        
        # Dummy chatbot reply
        reply = f"Hey {msg.user_id}, I hear you. Stay strong ❤️"

        # Save conversation in MongoDB
        chat_doc = {
            "user_id": msg.user_id,
            "message": msg.message,
            "bot_reply": reply,
            "timestamp": datetime.utcnow()
        }
        safe_db_operation(chat_collection.insert_one, chat_doc)

        return {"user": msg.message, "bot": reply}
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )

# 📌 New: Fetch chat history for a student
@router.get("/{user_id}")
def get_chat_history(user_id: str, current_user: User = Depends(get_current_active_user)):
    """Get chat history for the specified user."""
    try:
        # Ensure user can only access their own chat history
        if user_id != current_user.username:
            raise UnauthorizedAccessError("You can only access your own chat history")
        
        chats = list(safe_db_operation(chat_collection.find, {"user_id": user_id}, {"_id": 0}))
        return {"user_id": user_id, "history": chats, "count": len(chats)}
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chat history: {str(e)}"
        )
