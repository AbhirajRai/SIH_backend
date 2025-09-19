from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError
import os
import logging
from config import MONGODB_URL, LOG_LEVEL
from app.database_fallback import get_fallback_collection

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)

# Global variables for database connection
client = None
db = None
users_collection = None
moods_collection = None
chat_collection = None
streaks_collection = None

def connect_to_database():
    """Connect to MongoDB with error handling and retry logic."""
    global client, db, users_collection, moods_collection, chat_collection, streaks_collection
    
    try:
        # Create MongoDB client with optimized timeout settings
        client = MongoClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=15000,  # 15 second timeout
            connectTimeoutMS=15000,
            socketTimeoutMS=15000,
            retryWrites=True,
            maxPoolSize=5,
            retryReads=True,
            maxIdleTimeMS=30000,
            waitQueueTimeoutMS=10000,
            heartbeatFrequencyMS=10000
        )
        
        # Test the connection
        client.admin.command('ping')
        db = client["mindcare"]
        
        # Initialize collections
        users_collection = db["users"]
        moods_collection = db["moods"]
        chat_collection = db["chats"]
        streaks_collection = db["streaks"]
        
        logger.info("✅ Successfully connected to MongoDB")
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError) as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        logger.warning("🔄 Falling back to in-memory database for testing")
        # Initialize fallback collections
        users_collection = get_fallback_collection("users")
        moods_collection = get_fallback_collection("moods")
        chat_collection = get_fallback_collection("chats")
        streaks_collection = get_fallback_collection("streaks")
        return True
    except Exception as e:
        logger.error(f"❌ Unexpected database error: {e}")
        return False

# Initialize connection
connect_to_database()

# Create indexes for better performance
def create_indexes():
    """Create database indexes for better performance."""
    if db is None:
        logger.error("❌ Database not connected. Cannot create indexes.")
        return False
        
    try:
        # User collection indexes
        users_collection.create_index("username", unique=True)
        users_collection.create_index("email", unique=True)
        
        # Moods collection indexes
        moods_collection.create_index("user_id")
        moods_collection.create_index([("user_id", 1), ("timestamp", -1)])
        
        # Chat collection indexes
        chat_collection.create_index("user_id")
        chat_collection.create_index([("user_id", 1), ("timestamp", -1)])
        
        # Streaks collection indexes
        streaks_collection.create_index("user_id", unique=True)
        
        logger.info("✅ Database indexes created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating indexes: {e}")
        return False

# Initialize database
def init_database():
    """Initialize database with indexes."""
    if connect_to_database():
        create_indexes()
        return True
    return False

# Test database connection
def test_connection():
    """Test database connection."""
    try:
        if client is not None:
            client.admin.command('ping')
            logger.info("✅ Database connection successful")
            return True
        else:
            logger.error("❌ Database client not initialized")
            return False
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

# Database operation wrapper with error handling
def safe_db_operation(operation, *args, **kwargs):
    """Wrapper for database operations with error handling."""
    try:
        if db is None:
            raise ConnectionError("Database not connected")
        return operation(*args, **kwargs)
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        raise
