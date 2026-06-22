#!/usr/bin/env python3
# Bot with logging - Week 2 Day 4

import ollama
import logging

# Configure logging (simpler format)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BotWithLogging:
    def __init__(self, model='hermes3:3b', temperature=0.7):
        self.model = model
        self.temperature = temperature
        self.conversation_history = []
        logging.info(f"Bot initialized with model: {model}")
    
    def chat(self, user_message):
        logging.info(f"User: {user_message[:40]}...")
        
        self.conversation_history.append({'role': 'user', 'content': user_message})
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=self.conversation_history,
                options={'temperature': self.temperature}
            )
            
            bot_response = response['message']['content']
            self.conversation_history.append({'role': 'assistant', 'content': bot_response})
            
            logging.info(f"Bot: {bot_response[:40]}...")
            return bot_response
            
        except Exception as e:
            logging.error(f"Error: {e}")
            return "An error occurred."

# Demo
if __name__ == "__main__":
    print("=== Bot With Logging ===\n")
    
    bot = BotWithLogging()
    response = bot.chat("Say 'Hello from the logged bot!'")
    print(f"Bot: {response}\n")
    
    print("Check the log messages above.")
