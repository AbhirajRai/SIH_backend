from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re

class MoodLog(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50, description="User ID must be between 1-50 characters")
    mood: str = Field(..., min_length=1, max_length=20, description="Mood must be between 1-20 characters")
    note: Optional[str] = Field(None, max_length=500, description="Note must be less than 500 characters")
    
    @validator('mood')
    def validate_mood(cls, v):
        valid_moods = ['happy', 'sad', 'angry', 'anxious', 'excited', 'calm', 'stressed', 'confused', 'grateful', 'lonely', 'content', 'overwhelmed']
        if v.lower() not in valid_moods:
            raise ValueError(f'Mood must be one of: {", ".join(valid_moods)}')
        return v.lower()
    
    @validator('user_id')
    def validate_user_id(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('User ID can only contain letters, numbers, underscores, and hyphens')
        return v

class ChatMessage(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50, description="User ID must be between 1-50 characters")
    message: str = Field(..., min_length=1, max_length=1000, description="Message must be between 1-1000 characters")
    
    @validator('user_id')
    def validate_user_id(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('User ID can only contain letters, numbers, underscores, and hyphens')
        return v

# Authentication Models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, description="Username must be between 3-30 characters")
    email: str = Field(..., description="Valid email address required")
    password: str = Field(..., min_length=6, max_length=100, description="Password must be between 6-100 characters")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name must be less than 100 characters")
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.lower()
    
    @validator('email')
    def validate_email(cls, v):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, description="Username is required")
    password: str = Field(..., min_length=1, description="Password is required")

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Error Response Models
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ValidationErrorResponse(BaseModel):
    detail: list
    error_code: str = "VALIDATION_ERROR"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
