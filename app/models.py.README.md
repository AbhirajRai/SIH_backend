# models.py - Data Models and Validation

## What This File Does
This file defines all the data structures and validation rules for the MindCare API. It's like the "blueprint" that describes what data looks like and what rules it must follow.

## In Simple Terms
Think of this as the instruction manual that tells the API what information to expect, how to format it, and what rules to check before accepting it. It's like having a quality control inspector for all incoming data.

## Key Responsibilities

### 1. **Data Structure Definition**
- Defines what fields each data type should have
- Specifies data types (string, integer, boolean, etc.)
- Sets required vs optional fields

### 2. **Input Validation**
- Checks if data meets certain criteria
- Validates email formats, password strength, etc.
- Prevents invalid data from entering the system

### 3. **API Documentation**
- Automatically generates API documentation
- Shows clients what data to send
- Provides examples of valid data formats

## Data Models Explained

### 1. **MoodLog Model**
```python
class MoodLog(BaseModel):
    user_id: str  # Who is logging the mood
    mood: str     # What mood they're feeling
    note: Optional[str]  # Optional note about the mood
```

**Usage:** Used for creating new mood entries and retrieving mood history. Each mood log gets a unique ID when saved, which can be used to delete the entry later.

**Validation Rules:**
- `user_id`: Must be 1-50 characters, only letters/numbers/underscores/hyphens
- `mood`: Must be one of: happy, sad, angry, anxious, excited, calm, stressed, confused, grateful, lonely, content, overwhelmed
- `note`: Optional, maximum 500 characters

### 2. **ChatMessage Model**
```python
class ChatMessage(BaseModel):
    user_id: str    # Who is sending the message
    message: str    # The actual message content
```

**Validation Rules:**
- `user_id`: Must be 1-50 characters, only letters/numbers/underscores/hyphens
- `message`: Must be 1-1000 characters

### 3. **UserCreate Model (Registration)**
```python
class UserCreate(BaseModel):
    username: str      # Unique username
    email: str         # Valid email address
    password: str      # Secure password
    full_name: Optional[str]  # Optional real name
```

**Validation Rules:**
- `username`: 3-30 characters, only letters/numbers/underscores/hyphens
- `email`: Must be valid email format (user@domain.com)
- `password`: 6-100 characters, must contain at least one letter and one number
- `full_name`: Optional, maximum 100 characters

### 4. **UserLogin Model**
```python
class UserLogin(BaseModel):
    username: str  # Username for login
    password: str  # Password for login
```

**Validation Rules:**
- Both fields are required
- No additional format restrictions (security handled elsewhere)

### 5. **User Model (Response)**
```python
class User(BaseModel):
    id: Optional[str]        # Database ID
    username: str            # Username
    email: str               # Email address
    full_name: Optional[str] # Real name
    is_active: bool          # Account status
    created_at: Optional[datetime]  # When account was created
```

**Note:** This model is used for API responses and doesn't include the password hash for security.

## Validation Features

### 1. **Custom Validators**
```python
@validator('mood')
def validate_mood(cls, v):
    valid_moods = ['happy', 'sad', 'angry', 'anxious', 'excited', 'calm', 'stressed', 'confused', 'grateful', 'lonely', 'content', 'overwhelmed']
    if v.lower() not in valid_moods:
        raise ValueError(f'Mood must be one of: {", ".join(valid_moods)}')
    return v.lower()
```

### 2. **Email Validation**
```python
@validator('email')
def validate_email(cls, v):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, v):
        raise ValueError('Invalid email format')
    return v.lower()
```

### 3. **Password Strength**
```python
@validator('password')
def validate_password(cls, v):
    if len(v) < 6:
        raise ValueError('Password must be at least 6 characters long')
    if not re.search(r'[A-Za-z]', v):
        raise ValueError('Password must contain at least one letter')
    if not re.search(r'\d', v):
        raise ValueError('Password must contain at least one number')
    return v
```

### 4. **Username Format**
```python
@validator('username')
def validate_username(cls, v):
    if not re.match(r'^[a-zA-Z0-9_-]+$', v):
        raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
    return v.lower()
```

## Error Response Models

### 1. **ErrorResponse**
```python
class ErrorResponse(BaseModel):
    detail: str                    # Error message
    error_code: Optional[str]      # Error code for programmatic handling
    timestamp: datetime            # When the error occurred
```

### 2. **ValidationErrorResponse**
```python
class ValidationErrorResponse(BaseModel):
    detail: list                   # List of validation errors
    error_code: str = "VALIDATION_ERROR"
    timestamp: datetime            # When the error occurred
```

## How Validation Works

### 1. **Automatic Validation**
When a client sends data to the API:
```python
# Client sends this data
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "mypassword123"
}

# Pydantic automatically validates:
# - Username format and length
# - Email format
# - Password strength
# - Required fields
```

### 2. **Error Responses**
If validation fails:
```python
# API returns this error
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "password",
            "message": "Password must contain at least one letter",
            "type": "value_error"
        }
    ],
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Security Features

### 1. **Input Sanitization**
- Usernames and emails are converted to lowercase
- Special characters are restricted in usernames
- Password strength requirements prevent weak passwords

### 2. **Data Type Safety**
- All fields have specific data types
- Optional fields are clearly marked
- Prevents type-related errors

### 3. **Length Limits**
- Prevents extremely long inputs that could cause issues
- Reasonable limits for all text fields
- Protects against buffer overflow attacks

## Why This Structure Matters

### 1. **Data Consistency**
- All data follows the same format
- Prevents inconsistent data entry
- Makes the API predictable and reliable

### 2. **Security**
- Input validation prevents malicious data
- Password strength requirements
- Email format validation

### 3. **User Experience**
- Clear error messages when validation fails
- Automatic API documentation
- Consistent data formats

### 4. **Maintainability**
- Centralized validation rules
- Easy to modify validation criteria
- Clear separation of concerns

## Usage Examples

### In Route Handlers
```python
@router.post("/moods/")
def log_mood(mood: MoodLog, current_user: User = Depends(get_current_active_user)):
    # mood is automatically validated according to MoodLog model
    # If validation fails, FastAPI returns 422 error automatically
    pass
```

### Custom Validation
```python
# The validator automatically runs when creating a MoodLog
mood = MoodLog(
    user_id="john_doe",
    mood="happy",  # This will be validated against the allowed list
    note="Feeling great today!"
)
```

This models file provides a robust foundation for data validation, ensuring that all data entering the MindCare API is properly formatted, secure, and consistent.
