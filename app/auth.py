from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pymongo import MongoClient
from app.models import User, UserInDB, TokenData
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token
security = HTTPBearer()

# MongoDB connection
from app.database import users_collection

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def get_user(username: str) -> Optional[UserInDB]:
    """Get user from database by username."""
    if users_collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database not connected"
        )
    
    user_data = users_collection.find_one({"username": username})
    if user_data:
        user_data["id"] = str(user_data["_id"])
        return UserInDB(**user_data)
    return None

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate a user by username and password."""
    try:
        user = get_user(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    except HTTPException:
        # Re-raise HTTP exceptions (like database not connected)
        raise
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}"
        )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode a JWT token."""
    try:
        print(f"🔍 Verifying token: {token[:50]}...")
        print(f"🔍 Using SECRET_KEY: {SECRET_KEY[:20]}...")
        print(f"🔍 Using ALGORITHM: {ALGORITHM}")
        
        # Decode without verification first to see the payload
        unverified_payload = jwt.decode(token, options={"verify_signature": False}, key="")
        print(f"🔍 Unverified payload: {unverified_payload}")
        
        # Now verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"🔍 Verified payload: {payload}")
        
        username: str = payload.get("sub")
        if username is None:
            print("❌ No 'sub' field in token")
            return None
        
        token_data = TokenData(username=username)
        print(f"✅ Token valid for user: {username}")
        return token_data
    except JWTError as e:
        print(f"❌ JWT Error: {e}")
        print(f"❌ Token that failed: {token}")
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print(f"🔍 Getting current user with credentials: {credentials.credentials[:50]}...")
    
    token_data = verify_token(credentials.credentials)
    if token_data is None:
        print("❌ Token validation failed")
        raise credentials_exception
    
    print(f"🔍 Looking up user: {token_data.username}")
    user = get_user(username=token_data.username)
    if user is None:
        print(f"❌ User not found: {token_data.username}")
        raise credentials_exception
    
    print(f"✅ User found: {user.username}")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
