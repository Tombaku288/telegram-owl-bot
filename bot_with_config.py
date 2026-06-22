#!/usr/bin/env python3
# Bot that loads config from JSON - Week 2 Day 5

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

class ConfigBot:
    def __init__(self):
        self.model = config['model']
        self.temperature = config['temperature']
        self.max_tokens = config['max_tokens']
        self.conversation_history = [
            {'role': 'system', 'content': config['system_prompt']}
        ]
        logging.info(f"Bot initialized with model: {self.model}")
        logging.info(f"Temperature: {self.temperature}")
    
    def chat(self, user_message):
        logging.info(f"User: {user_message}")
        
        self.conversation_history.append({'role': 'user', 'content': user_message})
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=self.conversation_history,
                options={
                    'temperature': self.temperature,
                    'max_tokens': self.max_tokens
                }
            )
            
            bot_response = response['message']['content']
            self.conversation_history.append({'role': 'assistant', 'content': bot_response})
            
            logging.info(f"Bot: {bot_response}")
            return bot_response
            
        except Exception as e:
            logging.error(f"Error: {e}")
            return "An error occurred."

# Demo
if __name__ == "__main__":
    print("\n=== Bot With Config ===\n")
    
    bot = ConfigBot()
    
    response = bot.chat("What is your name?")
    print(f"Bot: {response}\n")
    
    response2 = bot.chat("What is my name?")
    print(f"Bot: {response2}\n")
    
    print("Try changing config.json and run again to see the difference!")
