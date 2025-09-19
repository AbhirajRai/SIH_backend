# database.py - Database Connection and Operations

## What This File Does
This file handles all database operations for the MindCare API. It's like the "librarian" that manages how the application talks to the MongoDB database.

## In Simple Terms
Think of this as the bridge between your application and the database. It establishes the connection, creates the necessary "shelves" (collections) for storing data, and provides safe ways to read and write information.

## Key Responsibilities

### 1. **Database Connection**
- Connects to MongoDB using the connection string from config
- Sets up connection timeouts and retry logic
- Tests the connection to make sure it's working
- Handles connection failures gracefully

### 2. **Collection Setup**
Creates and manages four main data collections:
- **users**: Stores user account information (username, email, password, etc.)
- **moods**: Stores mood logs with timestamps and notes
- **chats**: Stores chatbot conversation history
- **streaks**: Stores user streak counts for gamification

### 3. **Performance Optimization**
- Creates database indexes for faster queries
- Indexes on usernames, emails, user_ids, and timestamps
- Ensures unique constraints on usernames and emails

### 4. **Error Handling**
- Catches database connection errors
- Provides fallback mechanisms
- Logs errors for debugging
- Returns meaningful error messages

## How It Works

### Connection Process
```python
def connect_to_database():
    # 1. Create MongoDB client with timeout settings
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    
    # 2. Test the connection
    client.admin.command('ping')
    
    # 3. Select the database
    db = client["mindcare"]
    
    # 4. Initialize collections
    users_collection = db["users"]
    moods_collection = db["moods"]
    # ... etc
```

### Index Creation
```python
def create_indexes():
    # User collection indexes
    users_collection.create_index("username", unique=True)
    users_collection.create_index("email", unique=True)
    
    # Moods collection indexes
    moods_collection.create_index("user_id")
    moods_collection.create_index([("user_id", 1), ("timestamp", -1)])
```

### Safe Operations
```python
def safe_db_operation(operation, *args, **kwargs):
    # Wraps database operations with error handling
    try:
        if db is None:
            raise ConnectionError("Database not connected")
        return operation(*args, **kwargs)
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        raise
```

## Database Collections Explained

### 1. **Users Collection**
- Stores user account information
- Indexes: username (unique), email (unique)
- Fields: username, email, hashed_password, full_name, is_active, created_at

### 2. **Moods Collection**
- Stores mood tracking data
- Indexes: user_id, (user_id, timestamp)
- Fields: user_id, mood, note, timestamp

### 3. **Chats Collection**
- Stores chatbot conversation history
- Indexes: user_id, (user_id, timestamp)
- Fields: user_id, message, bot_reply, timestamp

### 4. **Streaks Collection**
- Stores user streak counts
- Indexes: user_id (unique)
- Fields: user_id, streak

## Error Handling Features

### Connection Errors
- **ConnectionFailure**: Database server is down
- **ServerSelectionTimeoutError**: Database is too slow to respond
- **ConfigurationError**: Invalid connection settings

### Graceful Degradation
- Logs errors instead of crashing
- Provides meaningful error messages
- Allows application to continue running even if database is temporarily unavailable

## Performance Features

### Indexes
- **Unique indexes**: Prevent duplicate usernames/emails
- **Compound indexes**: Speed up queries that filter by user_id and sort by timestamp
- **Single field indexes**: Speed up lookups by user_id

### Connection Pooling
- **maxPoolSize=10**: Allows up to 10 concurrent database connections
- **retryWrites=True**: Automatically retries failed write operations
- **Timeout settings**: Prevents hanging on slow database responses

## Why This Structure Matters

### 1. **Reliability**
- Handles database failures gracefully
- Provides fallback mechanisms
- Logs errors for debugging

### 2. **Performance**
- Database indexes speed up queries
- Connection pooling improves efficiency
- Timeout settings prevent hanging

### 3. **Maintainability**
- Centralized database logic
- Easy to modify connection settings
- Clear separation of concerns

### 4. **Security**
- Safe database operations prevent SQL injection
- Connection string validation
- Error handling prevents information leakage

## Usage Example
```python
from app.database import users_collection, safe_db_operation

# Safe way to insert a user
user_data = {"username": "john", "email": "john@example.com"}
result = safe_db_operation(users_collection.insert_one, user_data)

# Safe way to find a user
user = safe_db_operation(users_collection.find_one, {"username": "john"})
```

This database module provides a robust, performant, and secure foundation for all data operations in the MindCare API.
