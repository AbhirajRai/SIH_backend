# 🧠 SIH Backend - Mental Health API

A simple and powerful backend for student mental health tracking with AI-powered features.

## 🚀 What This Does

This backend helps students track their mental health by providing:
- **User accounts** - Sign up and login securely
- **Mood tracking** - Log daily moods and feelings
- **🗑️ Mood deletion** - Delete unwanted mood entries with security
- **AI chatbot** - Talk to an AI that understands mental health
- **Smart analysis** - AI analyzes your text for emotions and stress
- **Progress tracking** - See your mental health journey over time

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **MongoDB** - Database to store user data
- **JWT** - Secure user authentication
- **AI Models** - Pre-trained models for mental health analysis

## 📁 Project Structure

```
SIH_backend/
├── app/
│   ├── main.py              # Main application file
│   ├── auth.py              # User login/security
│   ├── database.py          # Database connection
│   ├── models.py            # Data structures
│   ├── nlp_services.py      # AI analysis functions
│   └── routes/              # API endpoints
│       ├── auth.py          # Login/register
│       ├── moods.py         # Mood tracking
│       ├── nlp.py           # AI analysis
│       └── chatbot.py       # AI chatbot
├── config.py                # Settings
└── requirements.txt         # Dependencies
```

## 🔧 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Test It Works
Visit: http://localhost:8000/docs

## 📡 Main API Endpoints

### 🔐 Authentication
- `POST /auth/register` - Create new account
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info

### 😊 Mood Tracking
- `POST /moods/` - Log a mood
- `GET /moods/{user_id}` - Get mood history
- `DELETE /moods/{mood_id}` - **Delete a mood log** 🆕

### 🤖 AI Features
- `POST /nlp/chatbot` - Chat with AI
- `POST /nlp/sentiment` - Analyze text emotions
- `POST /nlp/emotion` - Detect emotions
- `POST /nlp/toxicity` - Check for harmful content

### 🎯 Gamification
- `POST /gamify/streak/{user_id}` - Update daily streak
- `GET /gamify/streak/{user_id}` - Get streak info

## 🔒 Security Features

- **Password Protection** - Passwords are encrypted
- **JWT Tokens** - Secure user sessions
- **Input Validation** - All data is checked before saving
- **User Isolation** - Users can only see their own data

## 🧠 AI Features

The backend uses pre-trained AI models to:
- **Analyze emotions** in text messages
- **Detect stress** and mental health concerns
- **Provide smart responses** in the chatbot
- **Flag harmful content** for safety

## 🌐 Frontend Integration

This backend works with the frontend at `http://localhost:3000`:
- Login page connects to `/auth/login`
- Mood tracker saves to `/moods/`
- Chatbot talks through `/nlp/chatbot`

## 🚨 Important Notes

- **Database**: Uses MongoDB (cloud-hosted)
- **Port**: Runs on port 8000
- **Environment**: Development mode by default
- **CORS**: Enabled for localhost:3000

## 🐛 Troubleshooting

**Server won't start?**
- Check if port 8000 is free
- Make sure all dependencies are installed

**Database errors?**
- Check internet connection (MongoDB is cloud-hosted)
- Verify MongoDB URL in config.py

**AI features not working?**
- Models download automatically on first use
- May take a few minutes to load initially

## 📞 Support

If something breaks:
1. Check the terminal for error messages
2. Visit http://localhost:8000/docs for API help
3. Make sure frontend is running on port 3000

---

**That's it!** This backend makes mental health tracking simple and secure for students. 🎓💚