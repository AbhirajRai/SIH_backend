"""
Advanced Mental Health Chatbot with State Management
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from app.nlp_services import analyze_sentiment, analyze_emotion, analyze_distress

logger = logging.getLogger(__name__)

class MentalHealthChatbot:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.conversation_history: Dict[str, List[Dict]] = {}
        
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
    
    def _update_session(self, user_id: str, **kwargs):
        """Update session data."""
        if user_id in self.sessions:
            self.sessions[user_id].update(kwargs)
            self.sessions[user_id]["last_activity"] = datetime.utcnow()
    
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
    
    def get_reply(self, user_id: str, message: str) -> str:
        """Get chatbot response based on user message and current state."""
        try:
            # Cleanup old sessions
            self._cleanup_old_sessions()
            
            # Initialize session if new user
            if user_id not in self.sessions:
                self._initialize_session(user_id)
            
            session = self.sessions[user_id]
            state = session["state"]
            step = session["step"]
            
            # Analyze the message
            sentiment = analyze_sentiment(message)
            emotion = analyze_emotion(message)
            distress = analyze_distress(message)
            
            # Check for urgent distress
            if distress["is_urgent"]:
                response = self._handle_urgent_distress(message, distress)
                self._add_to_history(user_id, message, response, {
                    "sentiment": sentiment,
                    "emotion": emotion,
                    "distress": distress
                })
                return response
            
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
            else:
                response = self._handle_default(user_id, message, sentiment, emotion)
            
            # Add to history
            self._add_to_history(user_id, message, response, {
                "sentiment": sentiment,
                "emotion": emotion,
                "distress": distress
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Chatbot error for user {user_id}: {e}")
            return "I'm having trouble processing that right now. Please try again, and remember that I'm here to listen and support you."
    
    def _handle_urgent_distress(self, message: str, distress: Dict) -> str:
        """Handle urgent distress situations."""
        return (
            "I'm concerned about what you're sharing. Your safety is important. "
            "Please consider reaching out to a mental health professional or crisis hotline immediately. "
            "In the US, you can call 988 for the Suicide & Crisis Lifeline, or text HOME to 741741 for Crisis Text Line. "
            "You're not alone, and there are people who want to help. Would you like me to help you find resources?"
        )
    
    def _handle_greeting(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
        """Handle initial greeting and setup."""
        self._update_session(user_id, state="checking_in", step=1)
        
        greetings = [
            "Hi! I'm here to listen and support you. How are you feeling today?",
            "Hello! I'm glad you're here. Can you tell me how you're doing?",
            "Hi there! I'm here to help. What's on your mind today?"
        ]
        
        # Choose greeting based on sentiment
        if sentiment["label"].lower() in ["negative", "neg"]:
            return "Hi. I can sense you might be going through a tough time. I'm here to listen. What's been on your mind?"
        else:
            return greetings[0]
    
    def _handle_checking_in(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
        """Handle checking in about current feelings."""
        if sentiment["label"].lower() in ["negative", "neg"] or emotion["label"].lower() in ["sadness", "anger", "fear"]:
            self._update_session(user_id, state="exploring_feelings", step=2)
            return (
                "I can hear that you're going through a difficult time. "
                "It takes courage to share these feelings. Can you tell me more about what's been troubling you?"
            )
        else:
            self._update_session(user_id, state="providing_support", step=2)
            return (
                "It's good to hear that you're doing okay. "
                "Is there anything specific you'd like to talk about or work through today?"
            )
    
    def _handle_exploring_feelings(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
        """Handle exploring feelings in more detail."""
        self._update_session(user_id, state="providing_support", step=3)
        
        responses = [
            "Thank you for sharing that with me. It sounds like you're dealing with a lot right now. How long have you been feeling this way?",
            "I can hear how much this is affecting you. Have you tried any coping strategies that have helped in the past?",
            "That sounds really challenging. What do you think might help you feel a bit better right now?"
        ]
        
        return responses[0]
    
    def _handle_providing_support(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
        """Handle providing emotional support."""
        self._update_session(user_id, state="coping_strategies", step=4)
        
        if sentiment["score"] > 0.7:  # Strong sentiment
            return (
                "I can really feel the intensity of what you're experiencing. "
                "Remember, it's okay to feel this way, and you're not alone. "
                "Would you like to explore some coping strategies that might help?"
            )
        else:
            return (
                "I appreciate you opening up about this. "
                "Sometimes talking about our feelings can help us process them. "
                "What would be most helpful for you right now?"
            )
    
    def _handle_coping_strategies(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
        """Handle discussing coping strategies."""
        strategies = [
            "Here are some strategies that might help: deep breathing, going for a walk, or talking to someone you trust.",
            "Some people find journaling, meditation, or engaging in a favorite hobby helpful during difficult times.",
            "Consider reaching out to friends, family, or a mental health professional for additional support."
        ]
        
        return strategies[0] + " Is there anything specific you'd like to try?"
    
    def _handle_default(self, user_id: str, message: str, sentiment: Dict, emotion: Dict) -> str:
        """Handle default responses."""
        return (
            "I'm here to listen and support you. "
            "Can you tell me more about what you're experiencing or what you'd like to work through?"
        )
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a user."""
        if user_id not in self.conversation_history:
            return []
        
        history = self.conversation_history[user_id]
        return history[-limit:] if limit else history
    
    def reset_session(self, user_id: str):
        """Reset a user's conversation session."""
        if user_id in self.sessions:
            del self.sessions[user_id]
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]

# Global chatbot instance
chatbot = MentalHealthChatbot()
