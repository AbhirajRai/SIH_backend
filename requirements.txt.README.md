# requirements.txt - Python Dependencies

## What This File Does
This file lists all the Python packages (libraries) that the MindCare API needs to run. It's like a shopping list of software components that need to be installed.

## In Simple Terms
Think of this as a recipe that tells you exactly which ingredients (Python packages) you need to make the MindCare API work properly.

## Package Categories

### 1. **Web Framework & Server**
- **fastapi**: The main web framework for building the API
- **uvicorn**: The web server that runs the FastAPI application
- **python-multipart**: Handles file uploads and form data

### 2. **Database & Data Storage**
- **pymongo**: Python driver for connecting to MongoDB database
- **python-dotenv**: Loads configuration from .env files

### 3. **Authentication & Security**
- **python-jose[cryptography]**: Creates and verifies JWT tokens for user authentication
- **passlib[bcrypt]**: Securely hashes passwords using bcrypt algorithm
- **email-validator**: Validates email addresses

### 4. **HTTP & Networking**
- **requests**: Makes HTTP requests to external services
- **python-dotenv**: Manages environment variables

### 5. **AI & Machine Learning (NLP Dependencies)**
- **transformers**: Hugging Face library for AI models (sentiment analysis, emotion detection)
- **torch**: PyTorch deep learning framework (used by transformers)
- **nltk**: Natural Language Toolkit for text processing
- **scikit-learn**: Machine learning library for data analysis
- **numpy**: Numerical computing library (used by other ML packages)

## How to Use This File

### Installation
```bash
pip install -r requirements.txt
```

This command will:
1. Read the requirements.txt file
2. Download and install each package listed
3. Install the correct versions specified

### Version Specifications
- **>=4.21.0**: Install version 4.21.0 or higher
- **>=1.12.0**: Install version 1.12.0 or higher
- **>=3.7**: Install version 3.7 or higher

The `>=` symbol means "this version or newer" to ensure compatibility.

## Why These Packages Are Needed

### 1. **FastAPI & Uvicorn**
- FastAPI provides the web framework for building REST APIs
- Uvicorn is the ASGI server that runs the FastAPI application
- Together they handle HTTP requests and responses

### 2. **MongoDB (PyMongo)**
- Stores user data, mood logs, chat history, and streaks
- Provides the database backend for the application

### 3. **Authentication Packages**
- JWT tokens for secure user authentication
- Bcrypt for secure password hashing
- Email validation for user registration

### 4. **AI/ML Packages**
- Transformers: Pre-trained AI models for sentiment analysis and emotion detection
- PyTorch: Deep learning framework that powers the AI models
- NLTK: Natural language processing tools
- Scikit-learn: Machine learning algorithms for risk assessment
- NumPy: Mathematical operations for AI computations

## Package Relationships
Some packages depend on others:
- **transformers** needs **torch** to run AI models
- **scikit-learn** needs **numpy** for mathematical operations
- **python-jose** needs **cryptography** for secure token operations
- **passlib** needs **bcrypt** for password hashing

## Size Considerations
- **torch**: Large package (~2GB) - contains deep learning models
- **transformers**: Large package (~500MB) - contains AI model files
- **nltk**: Medium package (~100MB) - contains language data

## Alternative Installation
For production deployments, you might want to use:
```bash
pip install --no-cache-dir -r requirements.txt
```

This prevents caching of downloaded packages, useful for Docker containers.

This requirements file ensures that anyone can install the exact same dependencies and run the MindCare API successfully, regardless of their system configuration.
