#!/usr/bin/env python3
# Bot with file logging - Week 2 Day 4

import ollama
import logging
from datetime import datetime

# Create a log file with timestamp
log_filename = f"bot_log_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log"

# Configure logging to BOTH file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

class BotWithFileLogging:
    def __init__(self, model='hermes3:3b', temperature=0.7):
        self.model = model
        self.temperature = temperature
        self.conversation_history = []
        logging.info(f"Bot started with model: {model}")
    
    def chat(self, user_message):
        logging.info(f"User: {user_message[:50]}")
        
        self.conversation_history.append({'role': 'user', 'content': user_message})
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=self.conversation_history,
                options={'temperature': self.temperature}
            )
            
            bot_response = response['message']['content']
            self.conversation_history.append({'role': 'assistant', 'content': bot_response})
            
            logging.info(f"Bot: {bot_response[:50]}")
            return bot_response
            
        except Exception as e:
            logging.error(f"Error: {e}")
            return "An error occurred."

# Demo
if __name__ == "__main__":
    print("\n=== Bot With File Logging ===\n")
    
    bot = BotWithFileLogging()
    
    response = bot.chat("What is your name?")
    print(f"Bot: {response}\n")
    
    response2 = bot.chat("What did I just ask you?")
    print(f"Bot: {response2}\n")
    
    print(f"Logs saved to: {log_filename}")
    print("Check the file with: cat", log_filename)
