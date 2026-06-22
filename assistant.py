#!/usr/bin/env python3
# Command-Line AI Assistant - Week 2 Day 7
# Combines everything: config, logging, error handling, sessions

import ollama
import json
import logging
from datetime import datetime

# Setup logging
log_filename = f"assistant_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

# Load config
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    logging.info("Config loaded successfully")
except FileNotFoundError:
    logging.warning("config.json not found, using defaults")
    config = {
        "model": "hermes3:3b",
        "temperature": 0.7,
        "max_tokens": 500,
        "system_prompt": "You are a helpful assistant named Hermes."
    }

class Assistant:
    def __init__(self):
        self.model = config['model']
        self.temperature = config['temperature']
        self.max_tokens = config['max_tokens']
        self.system_prompt = config['system_prompt']
        self.sessions = {}
        logging.info(f"Assistant started with model: {self.model}")
    
    def get_session(self, user):
        if user not in self.sessions:
            self.sessions[user] = [
                {'role': 'system', 'content': self.system_prompt}
            ]
            logging.info(f"New session: {user}")
        return self.sessions[user]
    
    def chat(self, user, message):
        session = self.get_session(user)
        session.append({'role': 'user', 'content': message})
        
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
            return bot_response
        except Exception as e:
            logging.error(f"Error: {e}")
            return "Sorry, an error occurred."
    
    def clear(self, user):
        if user in self.sessions:
            self.sessions[user] = [{'role': 'system', 'content': self.system_prompt}]
            return "Session cleared."
        return "No session found."

# Main program
if __name__ == "__main__":
    print("\n" + "="*50)
    print("     HERMES AI ASSISTANT")
    print("="*50)
    print(f"Model: {config['model']}")
    print(f"Temperature: {config['temperature']}")
    print("Commands: /clear, /quit")
    print("="*50 + "\n")
    
    assistant = Assistant()
    user = "user1"
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == '/quit':
                print("Goodbye!")
                logging.info("Session ended")
                break
            elif user_input.lower() == '/clear':
                print(assistant.clear(user))
                continue
            elif not user_input:
                continue
            
            response = assistant.chat(user, user_input)
            print(f"Hermes: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print("An error occurred. Check logs.")
