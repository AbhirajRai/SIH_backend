"""
MindCare Backend Configuration
Environment variables and configuration settings
"""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secure-secret-key-change-this-in-production-12345")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Database Configuration
MONGODB_URL = os.getenv(
    "MONGODB_URL", 
    "mongodb+srv://mindcare_user:IrmKVH96TWThI26J@mindcareluster.ftrolml.mongodb.net/?retryWrites=true&w=majority&appName=MindCareluster"
)

# Application Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CORS Configuration - Allow all origins for network access
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") != "*" else ["*"]

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validation
if SECRET_KEY == "your-super-secure-secret-key-change-this-in-production-12345" and ENVIRONMENT == "production":
    raise ValueError("SECRET_KEY must be changed for production environment!")

if MONGODB_URL.startswith("mongodb+srv://mindcare_user:") and ENVIRONMENT == "production":
    print("⚠️  WARNING: Using default MongoDB credentials in production!")
