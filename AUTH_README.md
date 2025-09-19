# MindCare Backend - Authentication System

## Overview
This backend now includes a complete JWT-based authentication system with user registration and login functionality.

## Features
- ✅ User Registration
- ✅ User Login with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ Protected routes with JWT authentication
- ✅ User-specific data access control
- ✅ MongoDB integration for user storage

## API Endpoints

### Authentication Endpoints

#### Register User
```
POST /auth/register
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
}
```

#### Login User
```
POST /auth/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepassword"
}
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

#### Get Current User
```
GET /auth/me
Authorization: Bearer <your_jwt_token>
```

### Protected Endpoints

All the following endpoints now require authentication:

#### Moods
- `POST /moods/` - Log a mood (requires auth)
- `GET /moods/{user_id}` - Get mood history (requires auth, own data only)

#### Chatbot
- `POST /chatbot/` - Send message to chatbot (requires auth)
- `GET /chatbot/{user_id}` - Get chat history (requires auth, own data only)

#### Gamification
- `POST /gamify/streak/{user_id}` - Update streak (requires auth, own data only)
- `GET /gamify/streak/{user_id}` - Get streak (requires auth, own data only)

## Usage

### 1. Register a new user
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "testpassword",
       "full_name": "Test User"
     }'
```

### 2. Login to get JWT token
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "testpassword"
     }'
```

### 3. Use JWT token for protected endpoints
```bash
curl -X GET "http://localhost:8000/moods/testuser" \
     -H "Authorization: Bearer <your_jwt_token>"
```

## Security Features

1. **Password Hashing**: All passwords are hashed using bcrypt
2. **JWT Tokens**: Secure token-based authentication
3. **User Isolation**: Users can only access their own data
4. **Token Expiration**: JWT tokens expire after 30 minutes
5. **Input Validation**: All inputs are validated using Pydantic models

## Database Schema

### Users Collection
```json
{
    "_id": "ObjectId",
    "username": "string (unique)",
    "email": "string (unique)",
    "full_name": "string",
    "hashed_password": "string",
    "is_active": "boolean",
    "created_at": "datetime"
}
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload
```

3. Access the API documentation at: `http://localhost:8000/docs`

## Configuration

- JWT Secret Key: Change `SECRET_KEY` in `app/auth.py` for production
- Token Expiration: Modify `ACCESS_TOKEN_EXPIRE_MINUTES` in `app/auth.py`
- Database URL: Update `MONGODB_URL` in `app/database.py`

## Notes

- The application automatically creates database indexes on startup
- All existing endpoints now require authentication
- Users can only access their own data (moods, chats, streaks)
- The system maintains backward compatibility with existing data structure
