# config.py - Application Configuration

## What This File Does
This file contains all the configuration settings for the MindCare API. It's like the "settings panel" that controls how the application behaves.

## In Simple Terms
Think of this as the control center where you can adjust all the knobs and switches that make the application work properly - like database connections, security settings, and server options.

## Key Configuration Areas

### 1. **Security Settings**
- **SECRET_KEY**: A secret password used to create and verify JWT tokens
- **ALGORITHM**: The encryption method used for JWT tokens (HS256)
- **ACCESS_TOKEN_EXPIRE_MINUTES**: How long login tokens last (30 minutes)

### 2. **Database Configuration**
- **MONGODB_URL**: The connection string to connect to the MongoDB database
- Contains the database server address, username, password, and connection options

### 3. **Application Settings**
- **ENVIRONMENT**: Whether the app is running in development or production
- **DEBUG**: Whether to show detailed error messages (True for development)
- **HOST**: Which network interface the server listens on (0.0.0.0 means all interfaces)
- **PORT**: Which port number the server runs on (8000)

### 4. **CORS Configuration**
- **CORS_ORIGINS**: List of websites that are allowed to access this API
- Prevents unauthorized websites from making requests to the API

### 5. **Logging Configuration**
- **LOG_LEVEL**: How much detail to include in log messages (INFO, DEBUG, ERROR, etc.)

## How It Works

### Environment Variables
The file uses the `python-dotenv` library to load settings from a `.env` file:
```python
load_dotenv()  # Loads variables from .env file
SECRET_KEY = os.getenv("SECRET_KEY", "default-value")
```

### Default Values
Each setting has a default value in case the environment variable isn't set:
- If `SECRET_KEY` isn't provided, it uses a default (but warns in production)
- If `PORT` isn't specified, it defaults to 8000
- If `DEBUG` isn't set, it defaults to True

### Security Validation
The file includes safety checks:
- Warns if using default secret key in production
- Warns if using default database credentials in production
- Ensures critical settings are properly configured

## Why This Structure Matters

### 1. **Flexibility**
- Easy to change settings without modifying code
- Different settings for development vs production
- Environment-specific configurations

### 2. **Security**
- Sensitive information (like passwords) can be stored in environment variables
- Prevents accidentally committing secrets to code repositories
- Centralized security configuration

### 3. **Maintainability**
- All configuration in one place
- Easy to see what settings are available
- Clear documentation of what each setting does

### 4. **Deployment**
- Easy to deploy to different environments (dev, staging, production)
- Can use different databases, ports, or security settings per environment
- No code changes needed for different deployments

## Example Usage
```python
from config import SECRET_KEY, MONGODB_URL, DEBUG

# Use the configured values
if DEBUG:
    print("Running in debug mode")
    
# Connect to database using configured URL
client = MongoClient(MONGODB_URL)
```

This configuration system makes the application flexible, secure, and easy to deploy across different environments while keeping sensitive information safe.
