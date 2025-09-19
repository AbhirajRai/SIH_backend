# main.py - Application Entry Point

## What This File Does
This is the main entry point for the MindCare mental health API. It's like the "front door" of the application that sets up everything needed to run the server.

## In Simple Terms
Think of this file as the conductor of an orchestra - it brings together all the different parts of the application and makes sure they work together harmoniously.

## Key Responsibilities

### 1. **FastAPI Application Setup**
- Creates the main FastAPI application instance
- Sets up the API title, description, and version
- Configures CORS (Cross-Origin Resource Sharing) to allow web browsers to access the API

### 2. **Security and Authentication**
- Adds JWT authentication middleware
- Sets up exception handlers for various error scenarios
- Configures security headers and CORS policies

### 3. **Database Initialization**
- Connects to MongoDB database on startup
- Creates necessary database indexes for better performance
- Tests database connection to ensure it's working

### 4. **Route Registration**
- Connects all the API endpoints from different route files:
  - `/auth/*` - User login, registration, and authentication
  - `/moods/*` - Mood tracking and history
  - `/chatbot/*` - Basic chatbot interactions
  - `/gamify/*` - Streak tracking and gamification
  - `/nlp/*` - Advanced AI analysis and mental health detection

### 5. **Error Handling**
- Sets up comprehensive error handling for:
  - Database connection issues
  - User authentication problems
  - Invalid data validation
  - MongoDB-specific errors
  - General application errors

### 6. **Health Check**
- Provides a simple endpoint (`/`) that returns a status message
- Useful for checking if the API is running

## How It Works
1. When the server starts, it runs the `startup_event()` function
2. This function tests the database connection and initializes it
3. All the route files are imported and connected to the main app
4. Exception handlers are registered to catch and handle errors gracefully
5. The server is ready to accept requests from clients

## Why This Structure Matters
- **Modularity**: Each feature (auth, moods, chatbot, etc.) is in its own file
- **Maintainability**: Easy to add new features or modify existing ones
- **Error Handling**: Consistent error responses across the entire API
- **Security**: Centralized security configuration and authentication setup
- **Performance**: Database indexes are created automatically for faster queries

This file essentially transforms a collection of Python modules into a fully functional web API that can handle mental health tracking, AI analysis, and user management.
