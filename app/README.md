# App Directory - Core Application Logic

This directory contains the main application logic for the MindCare mental health API. Each file serves a specific purpose in the overall system.

## Files Overview

### Core Application Files
- **main.py** - The main FastAPI application entry point
- **config.py** - Configuration settings and environment variables
- **database.py** - Database connection and operations
- **models.py** - Data models and validation schemas
- **exceptions.py** - Custom exception handling
- **auth.py** - Authentication and authorization logic

### AI and NLP Files
- **nlp_config.py** - Configuration for AI models and mental health detection
- **nlp_models.py** - AI model loading and initialization
- **nlp_models_pydantic.py** - Data models for AI analysis responses
- **nlp_services.py** - Core AI analysis functions (sentiment, emotion, toxicity, distress)
- **advanced_chatbot.py** - Intelligent chatbot with conversation memory

### Routes Directory
The `routes/` subdirectory contains API endpoint definitions:
- **auth.py** - User authentication endpoints
- **moods.py** - Mood tracking endpoints (create, read, delete)
- **chatbot.py** - Basic chatbot endpoints
- **gamify.py** - Gamification and streak tracking
- **nlp.py** - Advanced AI analysis endpoints

## How It All Works Together

1. **main.py** starts the FastAPI application and connects all the routes
2. **config.py** provides configuration settings from environment variables
3. **database.py** handles MongoDB connections and operations
4. **auth.py** manages user authentication and JWT tokens
5. **models.py** defines data structures and validation rules
6. **exceptions.py** provides consistent error handling across the API
7. The AI files work together to provide mental health analysis and chatbot functionality
8. Route files define the actual API endpoints that clients can call

This modular structure makes the codebase maintainable and allows for easy testing and development of individual components.
