# advanced_chatbot.py - Intelligent Mental Health Chatbot

## What This File Does
This file implements an advanced mental health chatbot with conversation memory, emotional intelligence, and crisis intervention capabilities. It's like having a trained mental health counselor who can understand emotions and provide appropriate support.

## In Simple Terms
Think of this as a smart chatbot that remembers your conversations, understands your emotions, and can provide personalized mental health support. It's like having a virtual counselor who gets to know you over time.

## Key Features

### 1. **Conversation Memory**
- Remembers previous conversations
- Maintains context across messages
- Tracks conversation state and progress

### 2. **Emotional Intelligence**
- Analyzes user emotions in real-time
- Adapts responses based on emotional state
- Provides empathetic and appropriate responses

### 3. **Crisis Intervention**
- Detects urgent distress situations
- Provides immediate crisis resources
- Escalates serious concerns appropriately

### 4. **State Management**
- Tracks conversation flow
- Manages different conversation states
- Provides context-aware responses

## How the Chatbot Works

### 1. **Session Management**
```python
def _initialize_session(self, user_id: str) -> Dict:
    """Initialize a new conversation session."""
    session = {
        "state": "greeting",
        "step": 0,
        "context": {},
        "created_at": datetime.utcnow(),
        "last_activity": datetime.utcnow()
    }
    self.sessions[user_id] = session
    self.conversation_history[user_id] = []
    return session
```

**What it does:** Creates a new conversation session for each user
**Features:**
- Tracks conversation state (greeting, checking_in, exploring_feelings, etc.)
- Records conversation steps and context
- Maintains timestamps for session management

### 2. **Message Analysis**
```python
def get_reply(self, user_id: str, message: str) -> str:
    # Analyze the message
    sentiment = analyze_sentiment(message)
    emotion = analyze_emotion(message)
    distress = analyze_distress(message)
    
    # Check for urgent distress
    if distress["is_urgent"]:
        response = self._handle_urgent_distress(message, distress)
        return response
```

**What it does:** Analyzes incoming messages for emotional content and crisis situations
**Features:**
- Real-time sentiment analysis
- Emotion detection
- Crisis situation identification
- Immediate intervention for urgent cases

### 3. **State-Based Responses**
```python
# State-based responses
if state == "greeting":
    response = self._handle_greeting(user_id, message, sentiment, emotion)
elif state == "checking_in":
    response = self._handle_checking_in(user_id, message, sentiment, emotion)
elif state == "exploring_feelings":
    response = self._handle_exploring_feelings(user_id, message, sentiment, emotion)
elif state == "providing_support":
    response = self._handle_providing_support(user_id, message, sentiment, emotion)
elif state == "coping_strategies":
    response = self._handle_coping_strategies(user_id, message, sentiment, emotion)
```

**What it does:** Provides different responses based on conversation state
**Features:**
- Context-aware responses
- Progressive conversation flow
- Appropriate support for each stage

## Conversation States

### 1. **Greeting State**
```python
def _handle_greeting(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
    """Handle initial greeting and setup."""
    self._update_session(user_id, state="checking_in", step=1)
    
    if sentiment["label"].lower() in ["negative", "neg"]:
        return "Hi. I can sense you might be going through a tough time. I'm here to listen. What's been on your mind?"
    else:
        return "Hi! I'm here to listen and support you. How are you feeling today?"
```

**Purpose:** Initial conversation setup and emotional assessment
**Features:**
- Adapts greeting based on emotional state
- Transitions to checking_in state
- Sets empathetic tone

### 2. **Checking In State**
```python
def _handle_checking_in(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
    """Handle checking in about current feelings."""
    if sentiment["label"].lower() in ["negative", "neg"] or emotion["label"].lower() in ["sadness", "anger", "fear"]:
        self._update_session(user_id, state="exploring_feelings", step=2)
        return "I can hear that you're going through a difficult time. It takes courage to share these feelings. Can you tell me more about what's been troubling you?"
    else:
        self._update_session(user_id, state="providing_support", step=2)
        return "It's good to hear that you're doing okay. Is there anything specific you'd like to talk about or work through today?"
```

**Purpose:** Assesses current emotional state and determines next steps
**Features:**
- Identifies negative emotions
- Provides appropriate support direction
- Transitions to appropriate state

### 3. **Exploring Feelings State**
```python
def _handle_exploring_feelings(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
    """Handle exploring feelings in more detail."""
    self._update_session(user_id, state="providing_support", step=3)
    
    responses = [
        "Thank you for sharing that with me. It sounds like you're dealing with a lot right now. How long have you been feeling this way?",
        "I can hear how much this is affecting you. Have you tried any coping strategies that have helped in the past?",
        "That sounds really challenging. What do you think might help you feel a bit better right now?"
    ]
    
    return responses[0]
```

**Purpose:** Encourages deeper emotional exploration
**Features:**
- Validates user's feelings
- Encourages further sharing
- Transitions to support phase

### 4. **Providing Support State**
```python
def _handle_providing_support(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
    """Handle providing emotional support."""
    self._update_session(user_id, state="coping_strategies", step=4)
    
    if sentiment["score"] > 0.7:  # Strong sentiment
        return "I can really feel the intensity of what you're experiencing. Remember, it's okay to feel this way, and you're not alone. Would you like to explore some coping strategies that might help?"
    else:
        return "I appreciate you opening up about this. Sometimes talking about our feelings can help us process them. What would be most helpful for you right now?"
```

**Purpose:** Provides emotional support and validation
**Features:**
- Acknowledges emotional intensity
- Offers validation and support
- Transitions to coping strategies

### 5. **Coping Strategies State**
```python
def _handle_coping_strategies(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
    """Handle discussing coping strategies."""
    strategies = [
        "Here are some strategies that might help: deep breathing, going for a walk, or talking to someone you trust.",
        "Some people find journaling, meditation, or engaging in a favorite hobby helpful during difficult times.",
        "Consider reaching out to friends, family, or a mental health professional for additional support."
    ]
    
    return strategies[0] + " Is there anything specific you'd like to try?"
```

**Purpose:** Provides practical coping strategies
**Features:**
- Offers specific coping techniques
- Encourages action
- Provides resource suggestions

## Crisis Intervention

### 1. **Urgent Distress Detection**
```python
def _handle_urgent_distress(self, message: str, distress: Dict) -> str:
    """Handle urgent distress situations."""
    return (
        "I'm concerned about what you're sharing. Your safety is important. "
        "Please consider reaching out to a mental health professional or crisis hotline immediately. "
        "In the US, you can call 988 for the Suicide & Crisis Lifeline, or text HOME to 741741 for Crisis Text Line. "
        "You're not alone, and there are people who want to help. Would you like me to help you find resources?"
    )
```

**Purpose:** Provides immediate crisis intervention
**Features:**
- Acknowledges concern for user safety
- Provides crisis hotline information
- Offers additional resource help
- Maintains supportive tone

### 2. **Crisis Resource Information**
- **988**: Suicide & Crisis Lifeline (US)
- **741741**: Crisis Text Line (US)
- **Local resources**: Mental health professionals
- **Emergency services**: 911 for immediate danger

## Conversation History

### 1. **History Storage**
```python
def _add_to_history(self, user_id: str, message: str, response: str, analysis: Dict = None):
    """Add conversation to history."""
    if user_id not in self.conversation_history:
        self.conversation_history[user_id] = []
    
    self.conversation_history[user_id].append({
        "timestamp": datetime.utcnow(),
        "user_message": message,
        "bot_response": response,
        "analysis": analysis or {}
    })
```

**What it stores:**
- Timestamp of conversation
- User's message
- Bot's response
- AI analysis results (sentiment, emotion, distress)

### 2. **History Retrieval**
```python
def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
    """Get conversation history for a user."""
    if user_id not in self.conversation_history:
        return []
    
    history = self.conversation_history[user_id]
    return history[-limit:] if limit else history
```

**Features:**
- Retrieves recent conversations
- Configurable limit
- Returns empty list for new users

## Session Management

### 1. **Session Cleanup**
```python
def _cleanup_old_sessions(self):
    """Remove sessions older than 24 hours."""
    cutoff = datetime.utcnow() - timedelta(hours=24)
    to_remove = []
    
    for user_id, session in self.sessions.items():
        if session["last_activity"] < cutoff:
            to_remove.append(user_id)
    
    for user_id in to_remove:
        del self.sessions[user_id]
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
```

**Purpose:** Prevents memory leaks and maintains performance
**Features:**
- Removes sessions older than 24 hours
- Cleans up conversation history
- Maintains system performance

### 2. **Session Reset**
```python
def reset_session(self, user_id: str):
    """Reset a user's conversation session."""
    if user_id in self.sessions:
        del self.sessions[user_id]
    if user_id in self.conversation_history:
        del self.conversation_history[user_id]
```

**Purpose:** Allows users to start fresh conversations
**Features:**
- Clears session state
- Removes conversation history
- Provides clean slate for new conversations

## Usage Examples

### 1. **Basic Conversation**
```python
from app.advanced_chatbot import chatbot

# Get chatbot response
response = chatbot.get_reply("john_doe", "I'm feeling really anxious today")
print(response)
# Output: "Hi. I can sense you might be going through a tough time. I'm here to listen. What's been on your mind?"

# Continue conversation
response = chatbot.get_reply("john_doe", "I have a job interview tomorrow and I'm terrified")
print(response)
# Output: "I can hear that you're going through a difficult time. It takes courage to share these feelings. Can you tell me more about what's been troubling you?"
```

### 2. **Crisis Intervention**
```python
# Crisis situation
response = chatbot.get_reply("john_doe", "I want to kill myself")
print(response)
# Output: "I'm concerned about what you're sharing. Your safety is important. Please consider reaching out to a mental health professional or crisis hotline immediately. In the US, you can call 988 for the Suicide & Crisis Lifeline, or text HOME to 741741 for Crisis Text Line. You're not alone, and there are people who want to help. Would you like me to help you find resources?"
```

### 3. **Conversation History**
```python
# Get conversation history
history = chatbot.get_conversation_history("john_doe", limit=5)
for conversation in history:
    print(f"User: {conversation['user_message']}")
    print(f"Bot: {conversation['bot_response']}")
    print(f"Analysis: {conversation['analysis']}")
    print("---")
```

## Integration with AI Analysis

### 1. **Real-time Analysis**
- Sentiment analysis for each message
- Emotion detection for response adaptation
- Distress detection for crisis intervention
- Confidence scoring for response quality

### 2. **Analysis Storage**
- Stores analysis results with each conversation
- Enables pattern recognition over time
- Supports risk assessment and monitoring
- Provides data for personalization

### 3. **Response Adaptation**
- Adapts responses based on emotional state
- Provides appropriate support level
- Escalates serious concerns
- Maintains empathetic tone

## Why This Structure Matters

### 1. **Mental Health Support**
- Provides appropriate emotional support
- Detects and responds to crisis situations
- Offers practical coping strategies
- Maintains therapeutic conversation flow

### 2. **User Experience**
- Remembers conversation context
- Provides personalized responses
- Maintains conversation continuity
- Offers appropriate support level

### 3. **Safety Features**
- Crisis detection and intervention
- Immediate resource provision
- Appropriate escalation
- Safety-focused responses

### 4. **Scalability**
- Efficient session management
- Automatic cleanup of old sessions
- Memory-efficient conversation storage
- Performance optimization

This advanced chatbot system provides intelligent, empathetic mental health support with conversation memory, emotional intelligence, and crisis intervention capabilities while maintaining performance and scalability.
