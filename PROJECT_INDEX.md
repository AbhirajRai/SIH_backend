# SIH Backend - MindCare Mental Health API - Project Index

## 📋 Project Overview

**SIH Backend** is a comprehensive mental health tracking and support API built with FastAPI. It provides user authentication, mood tracking, AI-powered chatbot support, and advanced natural language processing for mental health detection.

### 🎯 Core Purpose
- **Mental Health Support**: AI-powered emotional analysis and crisis detection
- **User Management**: Secure authentication and data isolation
- **Mood Tracking**: Daily mood logging with analytics
- **Gamification**: Streak tracking to encourage consistent check-ins
- **Risk Assessment**: AI-powered risk scoring based on emotional patterns

## 🏗️ Architecture Overview

```
SIH_backend/
├── app/                          # Main application module
│   ├── main.py                   # FastAPI application entry point
│   ├── models.py                 # Pydantic data models
│   ├── database.py               # MongoDB connection and operations
│   ├── auth.py                   # JWT authentication logic
│   ├── exceptions.py             # Custom exception handlers
│   ├── advanced_chatbot.py       # AI-powered mental health chatbot
│   ├── nlp_services.py           # NLP analysis services
│   ├── nlp_models.py             # ML model initialization
│   ├── nlp_config.py             # NLP configuration settings
│   ├── nlp_models_pydantic.py    # NLP-specific Pydantic models
│   └── routes/                   # API route modules
│       ├── auth.py               # Authentication endpoints
│       ├── moods.py              # Mood tracking endpoints
│       ├── chatbot.py            # Basic chatbot endpoints
│       ├── nlp.py                # Advanced NLP endpoints
│       └── gamify.py             # Gamification endpoints
├── config.py                     # Application configuration
├── requirements.txt              # Python dependencies
├── test_auth.py                  # Authentication tests
├── test_error_handling.py        # Error handling tests
└── README.md                     # Project documentation
```

## 🔧 Technology Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.8+**: Programming language
- **Uvicorn**: ASGI server for running the application

### Database
- **MongoDB**: NoSQL database for storing user data, moods, and conversations
- **PyMongo**: MongoDB driver for Python

### Authentication & Security
- **JWT (JSON Web Tokens)**: Stateless authentication
- **Bcrypt**: Password hashing
- **Python-JOSE**: JWT token handling

### AI/ML & NLP
- **Transformers**: Hugging Face transformers library
- **PyTorch**: Deep learning framework
- **NLTK**: Natural language processing toolkit
- **Scikit-learn**: Machine learning utilities

### Models Used
- **Sentiment Analysis**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Emotion Detection**: `bhadresh-savani/distilbert-base-uncased-emotion`
- **Toxicity Detection**: `unitary/toxic-bert`

## 📁 File Structure & Components

### Core Application Files

#### `app/main.py`
- **Purpose**: FastAPI application entry point
- **Key Features**:
  - CORS middleware configuration
  - Exception handlers registration
  - Route inclusion
  - Database initialization on startup
- **Routes**: `/auth/*`, `/moods/*`, `/chatbot/*`, `/gamify/*`, `/nlp/*`

#### `app/models.py`
- **Purpose**: Pydantic data models for request/response validation
- **Key Models**:
  - `MoodLog`: Mood tracking data
  - `ChatMessage`: Chat message structure
  - `UserCreate`, `UserLogin`, `User`: User management
  - `Token`: JWT token response
  - `ErrorResponse`: Error handling

#### `app/database.py`
- **Purpose**: MongoDB connection and database operations
- **Key Features**:
  - Connection management with retry logic
  - Collection initialization (users, moods, chats, streaks)
  - Index creation for performance
  - Safe database operation wrapper
- **Collections**:
  - `users`: User accounts and authentication data
  - `moods`: Mood tracking entries
  - `chats`: Chat conversation history
  - `streaks`: Gamification streak data

#### `app/auth.py`
- **Purpose**: JWT authentication and user management
- **Key Functions**:
  - Password hashing/verification
  - JWT token creation/verification
  - User authentication
  - Current user dependency injection

### AI & NLP Components

#### `app/advanced_chatbot.py`
- **Purpose**: AI-powered mental health chatbot with state management
- **Key Features**:
  - Conversation state management
  - Emotional analysis integration
  - Crisis intervention detection
  - Session cleanup and history tracking
- **States**: greeting, checking_in, exploring_feelings, providing_support, coping_strategies

#### `app/nlp_services.py`
- **Purpose**: Core NLP analysis services
- **Key Functions**:
  - `analyze_sentiment()`: Sentiment analysis
  - `analyze_emotion()`: Emotion detection
  - `analyze_toxicity()`: Toxicity screening
  - `analyze_distress()`: Crisis detection
  - `calculate_risk_score()`: Risk assessment

#### `app/nlp_models.py`
- **Purpose**: ML model initialization and management
- **Key Features**:
  - Model loading with fallback options
  - NLTK integration for synonym detection
  - Error handling and logging

#### `app/nlp_config.py`
- **Purpose**: NLP configuration and settings
- **Key Settings**:
  - Model names and parameters
  - Risk assessment thresholds
  - Urgent distress keywords
  - Severe emotion categories

#### `app/nlp_models_pydantic.py`
- **Purpose**: Pydantic models for NLP API responses
- **Key Models**:
  - `SentimentResponse`, `EmotionResponse`
  - `ToxicityResponse`, `DistressResponse`
  - `RiskScoreResponse`, `ChatResponse`
  - `ComprehensiveAnalysisResponse`

### API Routes

#### `app/routes/auth.py`
- **Endpoints**:
  - `POST /auth/register`: User registration
  - `POST /auth/login`: User login
  - `POST /auth/token`: OAuth2 token endpoint
  - `GET /auth/me`: Get current user info
- **Features**: JWT token generation, user validation

#### `app/routes/moods.py`
- **Endpoints**:
  - `POST /moods/`: Log a new mood
  - `GET /moods/{user_id}`: Get mood history
- **Features**: User data isolation, mood validation

#### `app/routes/chatbot.py`
- **Endpoints**:
  - `POST /chatbot/`: Send message to basic chatbot
  - `GET /chatbot/{user_id}`: Get chat history
- **Features**: Simple chatbot responses, conversation storage

#### `app/routes/nlp.py`
- **Endpoints**:
  - `POST /nlp/sentiment`: Sentiment analysis
  - `POST /nlp/emotion`: Emotion analysis
  - `POST /nlp/toxicity`: Toxicity detection
  - `POST /nlp/distress`: Distress detection
  - `POST /nlp/analyze`: Comprehensive analysis
  - `POST /nlp/chatbot`: Advanced chatbot interaction
  - `POST /nlp/risk/sentiment`: Risk assessment from sentiment
  - `POST /nlp/risk/emotion`: Risk assessment from emotions
  - `GET /nlp/chatbot/history/{user_id}`: Conversation history
  - `POST /nlp/chatbot/reset/{user_id}`: Reset chatbot session
  - `GET /nlp/health`: NLP services health check

#### `app/routes/gamify.py`
- **Endpoints**:
  - `POST /gamify/streak/{user_id}`: Update streak
  - `GET /gamify/streak/{user_id}`: Get current streak
- **Features**: Streak tracking, user data isolation

### Configuration & Utilities

#### `config.py`
- **Purpose**: Application configuration management
- **Key Settings**:
  - JWT secret key and algorithm
  - MongoDB connection string
  - CORS origins
  - Environment variables
  - Security validations

#### `app/exceptions.py`
- **Purpose**: Custom exception handling
- **Key Features**:
  - Custom exception classes
  - Exception handlers for different error types
  - Structured error responses
  - Logging integration

## 🔐 Security Features

### Authentication
- **JWT Tokens**: Stateless authentication with configurable expiration
- **Password Hashing**: Bcrypt with salt for secure password storage
- **User Isolation**: Users can only access their own data

### Data Validation
- **Pydantic Models**: Comprehensive input validation
- **Field Constraints**: Length limits, format validation
- **Error Handling**: Structured error responses

### Database Security
- **Connection Security**: MongoDB with authentication
- **Index Optimization**: Performance and security indexes
- **Error Handling**: Graceful database error handling

## 🧠 AI & Mental Health Features

### Sentiment Analysis
- **Model**: Twitter RoBERTa base sentiment model
- **Output**: Positive/negative/neutral with confidence scores
- **Use Case**: General emotional state assessment

### Emotion Detection
- **Model**: DistilBERT emotion classification
- **Output**: Specific emotions (joy, sadness, anger, fear, etc.)
- **Use Case**: Detailed emotional analysis

### Toxicity Detection
- **Model**: Toxic-BERT
- **Output**: Toxicity probability and safety assessment
- **Use Case**: Content moderation and safety

### Distress Detection
- **Method**: Hybrid rule-based + ML approach
- **Features**: Urgent keyword detection, sentiment analysis
- **Use Case**: Crisis intervention and risk assessment

### Risk Assessment
- **Method**: Historical pattern analysis
- **Input**: Sentiment/emotion history
- **Output**: Risk scores and recommendations
- **Use Case**: Long-term mental health monitoring

### Advanced Chatbot
- **Features**: State management, emotional analysis, crisis detection
- **States**: Multi-stage conversation flow
- **Integration**: Real-time NLP analysis
- **Use Case**: Interactive mental health support

## 📊 API Endpoints Summary

### Authentication (`/auth`)
- User registration and login
- JWT token management
- User profile access

### Mood Tracking (`/moods`)
- Daily mood logging
- Mood history retrieval
- User-specific data access

### Basic Chatbot (`/chatbot`)
- Simple chat interactions
- Conversation history
- Basic support responses

### Advanced NLP (`/nlp`)
- Comprehensive text analysis
- Advanced chatbot with AI
- Risk assessment tools
- Crisis detection

### Gamification (`/gamify`)
- Streak tracking
- Progress monitoring
- Engagement features

## 🧪 Testing

### Test Files
- `test_auth.py`: Authentication flow testing
- `test_error_handling.py`: Error handling validation

### Test Coverage
- User registration and login
- JWT token validation
- Error response formats
- Database error handling

## 🚀 Deployment

### Environment Variables
- `SECRET_KEY`: JWT signing key
- `MONGODB_URL`: Database connection string
- `ENVIRONMENT`: Development/production mode
- `CORS_ORIGINS`: Allowed frontend origins

### Dependencies
- FastAPI and Uvicorn for web framework
- PyMongo for database operations
- Transformers and PyTorch for AI models
- NLTK for natural language processing
- JWT and bcrypt for authentication

## 📈 Performance Considerations

### Database Optimization
- Indexed queries for user data
- Connection pooling
- Timeout configurations

### AI Model Management
- Model caching and reuse
- Fallback model support
- Error handling for model failures

### API Performance
- Async/await patterns
- Efficient data serialization
- Structured error responses

## 🔍 Monitoring & Health Checks

### Health Endpoints
- `/`: Basic API health check
- `/nlp/health`: NLP services health check

### Logging
- Structured logging throughout the application
- Error tracking and monitoring
- Performance metrics

## 🎯 Use Cases

### Mental Health Applications
- Mood tracking and analytics
- AI-powered emotional support
- Crisis detection and intervention
- Progress monitoring

### Wellness Platforms
- Daily check-ins and streaks
- Emotional pattern recognition
- Personalized recommendations
- Community features

### Healthcare Systems
- Patient monitoring
- Risk assessment
- Treatment progress tracking
- Clinical decision support

### Educational Platforms
- Student wellness monitoring
- Stress detection
- Support resource recommendations
- Academic performance correlation

## 📚 Documentation

### API Documentation
- Auto-generated Swagger/OpenAPI docs at `/docs`
- ReDoc documentation at `/redoc`
- Comprehensive usage examples in `HOW_TO_USE.md`

### Code Documentation
- Inline comments and docstrings
- README files for each module
- Type hints throughout the codebase

This index provides a comprehensive overview of the SIH Backend project structure, components, and capabilities. The system is designed to be a robust, scalable solution for mental health applications with strong security, comprehensive AI features, and excellent developer experience.
