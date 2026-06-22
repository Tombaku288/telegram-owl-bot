#!/usr/bin/env python3
# Multi-user bot with separate sessions - Week 2 Day 6

import ollama
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

class MultiUserBot:
    def __init__(self):
        self.model = config['model']
        self.temperature = config['temperature']
        self.max_tokens = config['max_tokens']
        self.system_prompt = config['system_prompt']
        # Each user gets their own conversation history
        self.user_sessions = {}
        logging.info(f"Bot initialized with model: {self.model}")
    
    def get_or_create_session(self, user_id):
        """Get existing session or create new one for user"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = [
                {'role': 'system', 'content': self.system_prompt}
            ]
            logging.info(f"New session created for user: {user_id}")
        return self.user_sessions[user_id]
    
    def chat(self, user_id, user_message):
        """Handle chat for a specific user"""
        logging.info(f"User {user_id}: {user_message}")
        
        # Get user's conversation history
        session = self.get_or_create_session(user_id)
        
        # Add user message
        session.append({'role': 'user', 'content': user_message})
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=session,
                options={
                    'temperature': self.temperature,
                    'max_tokens': self.max_tokens
                }
            )
            
            bot_response = response['message']['content']
            session.append({'role': 'assistant', 'content': bot_response})
            
            logging.info(f"User {user_id} response: {bot_response[:50]}...")
            return bot_response
            
        except Exception as e:
            logging.error(f"Error for user {user_id}: {e}")
            return "An error occurred."
    
    def clear_session(self, user_id):
        """Clear a user's conversation history"""
        if user_id in self.user_sessions:
            self.user_sessions[user_id] = [
                {'role': 'system', 'content': self.system_prompt}
            ]
            logging.info(f"Session cleared for user: {user_id}")
            return "Session cleared."
        return "User not found."

# Demo
if __name__ == "__main__":
    print("\n=== Multi-User Bot Demo ===\n")
    
    bot = MultiUserBot()
    
    # Simulate 2 different users
    print("--- User 1 (Alice) ---")
    response = bot.chat("alice", "My name is Alice")
    print(f"Bot: {response}\n")
    
    response = bot.chat("alice", "What is my name?")
    print(f"Bot: {response}\n")
    
    print("--- User 2 (Bob) ---")
    response = bot.chat("bob", "My name is Bob")
    print(f"Bot: {response}\n")
    
    response = bot.chat("bob", "What is my name?")
    print(f"Bot: {response}\n")
    
    # Check sessions
    print("--- Session Summary ---")
    print(f"Active sessions: {list(bot.user_sessions.keys())}")
    for user, session in bot.user_sessions.items():
        print(f"  {user}: {len(session)} messages stored")
