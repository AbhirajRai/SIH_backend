from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure, ServerSelectionTimeoutError
from app.models import UserCreate, UserLogin, User, Token
from app.auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash, 
    get_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user
)
from app.exceptions import (
    DatabaseConnectionError, UserNotFoundError, InvalidCredentialsError,
    DuplicateUserError, UnauthorizedAccessError
)
from app.database import users_collection, safe_db_operation

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = get_user(user.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = safe_db_operation(users_collection.find_one, {"email": user.email})
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = get_password_hash(user.password)
        user_data = {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        result = safe_db_operation(users_collection.insert_one, user_data)
        user_data["id"] = str(result.inserted_id)
        
        # Return user without password
        return User(**{k: v for k, v in user_data.items() if k != "hashed_password"})
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except DuplicateKeyError:
        raise DuplicateUserError("User with this information already exists")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and return JWT token."""
    try:
        user = authenticate_user(user_credentials.username, user_credentials.password)
        if not user:
            raise InvalidCredentialsError("Incorrect username or password")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Alternative login endpoint using OAuth2PasswordRequestForm (for FastAPI docs)."""
    try:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise InvalidCredentialsError("Incorrect username or password")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token generation failed: {str(e)}"
        )

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    try:
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user information: {str(e)}"
        )

@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """Example protected endpoint."""
    try:
        return [{"item_id": "Foo", "owner": current_user.username}]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve items: {str(e)}"
        )
