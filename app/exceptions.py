from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pymongo.errors import DuplicateKeyError, ConnectionFailure, ServerSelectionTimeoutError
from pydantic import ValidationError
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Custom Exception Classes
class DatabaseConnectionError(Exception):
    """Raised when database connection fails"""
    pass

class UserNotFoundError(Exception):
    """Raised when user is not found"""
    pass

class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid"""
    pass

class DuplicateUserError(Exception):
    """Raised when trying to create a user that already exists"""
    pass

class UnauthorizedAccessError(Exception):
    """Raised when user tries to access data they don't own"""
    pass

# Exception Handlers
async def database_connection_handler(request: Request, exc: DatabaseConnectionError):
    """Handle database connection errors"""
    logger.error(f"Database connection error: {exc}")
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Database service temporarily unavailable. Please try again later.",
            "error_code": "DATABASE_CONNECTION_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    """Handle user not found errors"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "User not found",
            "error_code": "USER_NOT_FOUND",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    """Handle invalid credentials errors"""
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid username or password",
            "error_code": "INVALID_CREDENTIALS",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def duplicate_user_handler(request: Request, exc: DuplicateUserError):
    """Handle duplicate user errors"""
    return JSONResponse(
        status_code=400,
        content={
            "detail": "User with this username or email already exists",
            "error_code": "DUPLICATE_USER",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def unauthorized_access_handler(request: Request, exc: UnauthorizedAccessError):
    """Handle unauthorized access errors"""
    return JSONResponse(
        status_code=403,
        content={
            "detail": "You can only access your own data",
            "error_code": "UNAUTHORIZED_ACCESS",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append({
            "field": field,
            "message": message,
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": errors,
            "error_code": "VALIDATION_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def mongodb_duplicate_key_handler(request: Request, exc: DuplicateKeyError):
    """Handle MongoDB duplicate key errors"""
    logger.error(f"MongoDB duplicate key error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "detail": "A record with this information already exists",
            "error_code": "DUPLICATE_KEY_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def mongodb_connection_handler(request: Request, exc: ConnectionFailure):
    """Handle MongoDB connection failures"""
    logger.error(f"MongoDB connection failure: {exc}")
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Database service temporarily unavailable. Please try again later.",
            "error_code": "MONGODB_CONNECTION_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def mongodb_timeout_handler(request: Request, exc: ServerSelectionTimeoutError):
    """Handle MongoDB timeout errors"""
    logger.error(f"MongoDB timeout error: {exc}")
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Database request timed out. Please try again later.",
            "error_code": "MONGODB_TIMEOUT_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred. Please try again later.",
            "error_code": "INTERNAL_SERVER_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
