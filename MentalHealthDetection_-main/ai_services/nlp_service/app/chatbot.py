# ai_services/nlp_service/app/chatbot.py

from typing import Dict

# Simple example dialogue states with empathetic and CBT-like responses
class Chatbot:
    def __init__(self):
        self.sessions: Dict[str, int] = {}  # track user session states

    def get_reply(self, user_id: str, message: str) -> str:
        # Initialize session state
        state = self.sessions.get(user_id, 0)

        message_lower = message.lower()

        # Basic state machine for demo
        if state == 0:
            self.sessions[user_id] = 1
            return ("Hi! I'm here to listen and support you. "
                    "Can you tell me how you're feeling today?")
        elif state == 1:
            # Very simple keyword-based empathetic response
            if any(word in message_lower for word in ["sad", "depressed", "unhappy", "down"]):
                self.sessions[user_id] = 2
                return ("I'm sorry to hear that. Sometimes talking about what's troubling you helps. "
                        "Would you like to share more?")
            else:
                self.sessions[user_id] = 1
                return ("Thanks for sharing! Could you tell me more about how you are feeling?")
        elif state == 2:
            # Offer simple CBT-like advice or encourage reflection
            if any(word in message_lower for word in ["yes", "sure", "okay"]):
                return ("Thank you for trusting me. Remember, it's okay to feel this way, "
                        "and small steps like mindfulness or journaling can help.")
            else:
                self.sessions[user_id] = 0  # reset session
                return ("That's okay. I'm here whenever you want to talk.")

chatbot = Chatbot()
