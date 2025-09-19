import warnings
import logging
import os
import sys

# Suppress ALL warnings before importing other modules
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Set logging levels for noisy modules
logging.getLogger("transformers").setLevel(logging.CRITICAL)
logging.getLogger("transformers.modeling_utils").setLevel(logging.CRITICAL)
logging.getLogger("transformers.configuration_utils").setLevel(logging.CRITICAL)
logging.getLogger("transformers.tokenization_utils").setLevel(logging.CRITICAL)
logging.getLogger("transformers.modeling_roberta").setLevel(logging.CRITICAL)
logging.getLogger("torch").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import DuplicateKeyError, ConnectionFailure, ServerSelectionTimeoutError
from app.routes import moods, chatbot, gamify, auth, nlp
from app.database import init_database, test_connection
from app.exceptions import (
    DatabaseConnectionError, UserNotFoundError, InvalidCredentialsError,
    DuplicateUserError, UnauthorizedAccessError,
    database_connection_handler, user_not_found_handler, invalid_credentials_handler,
    duplicate_user_handler, unauthorized_access_handler, validation_exception_handler,
    mongodb_duplicate_key_handler, mongodb_connection_handler, mongodb_timeout_handler,
    general_exception_handler
)
from config import CORS_ORIGINS, ENVIRONMENT

app = FastAPI(
    title="MindCare Backend Prototype",
    description="A mental health tracking API with JWT authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if ENVIRONMENT == "development" else CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(DatabaseConnectionError, database_connection_handler)
app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
app.add_exception_handler(DuplicateUserError, duplicate_user_handler)
app.add_exception_handler(UnauthorizedAccessError, unauthorized_access_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(DuplicateKeyError, mongodb_duplicate_key_handler)
app.add_exception_handler(ConnectionFailure, mongodb_connection_handler)
app.add_exception_handler(ServerSelectionTimeoutError, mongodb_timeout_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    if not test_connection():
        raise DatabaseConnectionError("Failed to connect to database")
    if not init_database():
        raise DatabaseConnectionError("Failed to initialize database")

# Connect routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(moods.router, prefix="/moods", tags=["Moods"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Basic Chatbot"])
app.include_router(gamify.router, prefix="/gamify", tags=["Gamification"])
app.include_router(nlp.router, prefix="/nlp", tags=["NLP & Mental Health AI"])

@app.get("/")
def root():
    return {"message": "MindCare API is running 🚀"}
